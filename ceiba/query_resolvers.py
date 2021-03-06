"""Module to resolve the queries.

API
---

.. autofunction:: resolver_query_properties
.. autofunction:: resolver_query_jobs

"""
from typing import Any, Dict, List, Optional

from more_itertools import take
from tartiflette import Resolver


__all__ = ["resolver_query_jobs", "resolver_query_properties", "resolver_query_collections"]


@Resolver("Query.properties")
async def resolver_query_properties(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Resolver in charge of returning Properties based on their `collection_name`.

    Parameters
    ----------
    paren
        initial value filled in to the engine `execute` method
    args
        computed arguments related to the field
    ctx
        context filled in at engine initialization
    info
        information related to the execution and field resolution

    Returns
    -------
    The list of all jobs with the given status.
    """
    collection = ctx["mongodb"][args["collection_name"]]
    data = collection.find()
    return list(data)


@Resolver("Query.jobs")
async def resolver_query_jobs(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Resolver in charge of returning jobs based on their status.

    Parameters
    ----------
    paren
        initial value filled in to the engine `execute` method
    args
        computed arguments related to the field
    ctx
        context filled in at engine initialization
    info
        information related to the execution and field resolution

    Returns
    -------
    The list of all jobs with the given status.
    """
    # metadata to query the jobs
    query = {"status": args["status"]}

    property_collection = args["collection_name"]
    jobs_collection = f"jobs_{property_collection}"
    collection = ctx["mongodb"][jobs_collection]

    # Return the first available jobs
    data = collection.find(query)

    if args["max_jobs"] is not None:
        jobs = take(args["max_jobs"], data)
    else:
        jobs = list(data)

    return jobs


@Resolver("Query.collections")
async def resolver_query_collections(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Resolver in charge of returning the available collections.

    Parameters
    ----------
    paren
        initial value filled in to the engine `execute` method
    args
        computed arguments related to the field
    ctx
        context filled in at engine initialization
    info
        information related to the execution and field resolution

    Returns
    -------
    The list of all available collection and their size

"""
    db = ctx["mongodb"]
    # Filter the names that are not in the reserved keywords
    reserved = {"jobs", "users"}
    names = filter(lambda name: all(r not in name for r in reserved), db.list_collection_names())

    return [{"name": name, "size": db[name].estimated_document_count()} for name in names]
