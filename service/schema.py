import graphene
import todo.schema

class Query(
    todo.schema.Query,
    graphene.ObjectType
):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

class Mutation(
    todo.schema.Mutation,
    graphene.ObjectType
):
    # This class will inherit from multiple Mutations
    # as we begin to add more apps to our project
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
