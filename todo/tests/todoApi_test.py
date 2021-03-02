import factory
import json
import random
from faker import Factory
from graphene_django.utils.testing import GraphQLTestCase
from graphene_django.utils.utils import camelize
from graphql_relay import to_global_id

from .factories import TodoFactory
from todo.models import Todo
from todo.types import TodoNode

faker = Factory.create()

class TodoApi_Test(GraphQLTestCase):
    def setUp(self):
        self.GRAPHQL_URL = "/todo/graphql"
        TodoFactory.create_batch(size=3)

    def test_create_todo(self):
        """
        Ensure we can create a new todo object.
        """
        todo_dict = camelize(factory.build(dict, FACTORY_CLASS=TodoFactory))

        response = self.query(
            """
            mutation($input: CreateTodoInput!) {
                createTodoApi(input: $input) {
                    clientMutationId,
                    todo {
                        id
                        date
                        text
                        done
                    }
                }
            }
            """,
            input_data={'data': todo_dict}
        )
        content = json.loads(response.content)
        generated_todo = content['data']['createTodoApi']['todo']
        self.assertResponseNoErrors(response)
        self.assertEquals(to_global_id(TodoNode._meta.name, todo_dict['id']), generated_todo['id'])
        self.assertEquals(todo_dict['date'], generated_todo['date'])
        self.assertEquals(todo_dict['text'], generated_todo['text'])
        self.assertEquals(todo_dict['done'], generated_todo['done'])

    def test_fetch_all(self):
        """
        Create 3 objects, fetch all using allTodoApi query and check that the 3 objects are returned following
        Relay standards.
        """
        response = self.query(
            """
            query {
                allTodoApi{
                    edges{
                        node{
                            id
                            date
                            text
                            done
                        }
                    }
                }
            }
            """
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        todos = content['data']['allTodoApi']['edges']
        todos_qs = Todo.objects.all()
        for i, edge in enumerate(todos):
            todo = edge['node']
            self.assertEquals(todo['id'], to_global_id(TodoNode._meta.name, todos_qs[i].id))
            self.assertEquals(todo['date'], str(todos_qs[i].date))
            self.assertEquals(todo['text'], todos_qs[i].text)
            self.assertEquals(todo['done'], todos_qs[i].done)

    def test_delete_mutation(self):
        """
        Create 3 objects, fetch all using allTodoApi query and check that the 3 objects are returned.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        list_query = """
            query {
                allTodoApi{
                    edges{
                        node{
                            id
                        }
                    }
                }
            }
            """
        response = self.query(list_query)
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        todos = content['data']['allTodoApi']['edges']
        todo_count = len(todos)
        for i, edge in enumerate(todos, start=1):
            todo = edge['node']
            todo_id = todo['id']
            response = self.query(
                """
                mutation($input:DeleteTodoInput!) {
                   deleteTodoApi(input: $input)
                   {
                       ok
                    }
                }
                """, input_data={'id': todo_id})
            response = self.query(list_query)
            content = json.loads(response.content)
            todos = content['data']['allTodoApi']['edges']
            new_len = len(todos)
            assert todo_count - i == new_len


    def test_update_mutation_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        todo = TodoFactory.create()
        todo_id = to_global_id(TodoNode._meta.name, todo.pk)
        todo_dict = factory.build(dict, FACTORY_CLASS=TodoFactory)
        response = self.query(
            """
            mutation($input: UpdateTodoInput!){
                updateTodoApi(input: $input) {
                    todo{
                        date
                        text
                        done
                    }
                }
            }
            """,
            input_data={
                'id': todo_id,
                'data': {
                    'date': todo_dict['date'],
                    'text': todo_dict['text'],
                    'done': todo_dict['done'],
                }
            }
        )
        self.assertResponseNoErrors(response)
        response = self.query(
            """
            query($id: ID!) {
                todoApi(id:$id){
                    date
                    text
                    done
                }
            }
            """,
            variables={'id': todo_id})
        parsed_response = json.loads(response.content)
        updated_todo_data = parsed_response['data']['todoApi']
        self.assertEquals(updated_todo_data['date'], todo_dict['date'])
        self.assertEquals(updated_todo_data['text'], todo_dict['text'])
        self.assertEquals(updated_todo_data['done'], todo_dict['done'])
        
    def test_update_mutation_date_with_incorrect_value_data_type(self):
        """
        Add an object. Call an update with 2 (or more) fields updated with values that are expected to fail.
        Fetch the object back and confirm that the fields were not updated (even partially).
        """
        todo = TodoFactory.create()
        todo_id = to_global_id(TodoNode._meta.name, todo.pk)
        random_int = faker.pyint()
        response = self.query(
            """
            mutation{
                updateTodoApi(input: {
                    id: "%s",
                    data:{
                        date: %s
                    }
                }) {
                    todoApi{
                        date
                    }
                }
            }
            """
        )
        self.assertResponseHasErrors(response)
    def test_update_mutation_text_with_incorrect_value_data_type(self):
        """
        Add an object. Call an update with 2 (or more) fields updated with values that are expected to fail.
        Fetch the object back and confirm that the fields were not updated (even partially).
        """
        todo = TodoFactory.create()
        todo_id = to_global_id(TodoNode._meta.name, todo.pk)
        random_int = faker.pyint()
        response = self.query(
            """
            mutation{
                updateTodoApi(input: {
                    id: "%s",
                    data:{
                        text: %s
                    }
                }) {
                    todoApi{
                        text
                    }
                }
            }
            """
        )
        self.assertResponseHasErrors(response)
    def test_update_mutation_done_with_incorrect_value_data_type(self):
        """
        Add an object. Call an update with 2 (or more) fields updated with values that are expected to fail.
        Fetch the object back and confirm that the fields were not updated (even partially).
        """
        todo = TodoFactory.create()
        todo_id = to_global_id(TodoNode._meta.name, todo.pk)
        response = self.query(
            """
            mutation{
                updateTodoApi(input: {
                    id: "%s",
                    data:{
                        done: %s
                    }
                }) {
                    todoApi{
                        done
                    }
                }
            }
            """
        )
        self.assertResponseHasErrors(response)

