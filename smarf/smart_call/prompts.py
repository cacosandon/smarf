from textwrap import dedent

from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam

from smarf.utils.get_data_around_call import CallData


class SmartCallPrompt:
    @staticmethod
    def get_user_message(call_data: CallData) -> ChatCompletionMessageParam:
        prompt = dedent(
            f"""\
            You are an intelligent code generator with context awareness.

            Your task is to produce executable Python code that will serve as the return value for the `smart_call` function, without using any external libraries.

            Remember that the context code could involve multiple `smart_call` invocations, but we are generating code for just one specific call. Your generated code MUST BE independent and focused on the current `smart_call` invocation, based on line number.

            This code is for one-time use, so be as efficient as possible. If there is no need to perform logic operations, you MUST return the expected result directly.

            You will receive two key pieces of information:
            1. The surrounding code where 'smart_call' is invoked.
            2. The variables available within the scope of the 'smart_call' function.

            You have full access to use any of these variables in your generated code. Note that these variables are already defined in the scope of the 'smart_call' function, so you MUST NOT define them again.

            To help you understand the expected output, please review the following examples:

            ### Example 1:

            <input_code>
            def save_record(id: str, description: str):
                post = Post.objects.get(id=id)
                post.description = description
                post.title = smart_call()
                post.save()
            </input_code>

            <variables>
            {{ 'id': '123', 'description': 'I love pineapples, because they can be a pizza topping' }}
            </variables>

            Output:

            ```
            return 'Love for pineapples'
            ```

            ### Example 2:

            <input_code>
            game_title = 'Tic Tac Toe'
            game_data = smart_call()

            game_description = game_data['description']
            game_players_count = game_data['players_count']
            starting_player = game_data['starting_player']
            </input_code>

            <variables>
            {{ 'game_title': 'The Legend of Zelda: Breath of the Wild' }}
            </variables>

            Output:

            ```
            import random

            return {{
                'description': 'Tic Tac Toe is a game that consists of a 3x3 grid. Players take turns marking the spaces in the grid with X or O. The player who succeeds in placing three of their marks in a horizontal, vertical, or diagonal row is the winner.',
                'players_count': 2,
                'starting_player': random.choice(['X', 'O']),
            }}
            ```

            ### Example 3:

            <input_code>
            prices = [{{ 'product_id': 1, 'price': 100 }}, {{ 'product_id': 2, 'price': 200 }}, {{ 'product_id': 3, 'price': 300 }}]
            total = smart_call()
            </input_code>

            <variables>
            {{ 'prices': [{{ 'product_id': 1, 'price': 100 }}, {{ 'product_id': 2, 'price': 200 }}, {{ 'product_id': 3, 'price': 300 }}] }}
            </variables>

            Output:

            ```
            return reduce(lambda total, price: total + price['price'], prices, 0)
            ```

            Now, you will receive the actual code where 'smart_call' is invoked:

            <input_code>
            {call_data.code}
            </input_code>

            These are the variables available within the scope of 'smart_call':

            <variables>
            {call_data.variables}
            </variables>

            Return the code that will be returned by the 'smart_call' function, and nothing else.
            """
        )

        return {
            "role": "user",
            "content": prompt,
        }
