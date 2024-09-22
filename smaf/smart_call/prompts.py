from textwrap import dedent

from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam

from smaf.utils.get_data_around_call import CallData


class SmartCallPrompt:
    @staticmethod
    def get_user_message(call_data: CallData) -> ChatCompletionMessageParam:
        prompt = dedent(
            f"""\
            You are an intelligent code generator with context awareness.

            Your task is to produce executable Python code that will serve as the return value for the 'smart_call' function, without using any external libraries.

            This code is for one-time use, so be as efficient as possible.

            You will receive two key pieces of information:
            1. The surrounding code where 'smart_call' is invoked.
            2. The variables available within the scope of the 'smart_call' function.

            You have full access to use any of these variables in your generated code.

            To help you understand the expected output, please review the following examples:

            Example 1:

            <input_code>
            def save_record(id: str, description: str):
                post = Post.objects.get(id=id)
                post.description = description
                post.title = smart_call()
                post.save()
            </input_code>

            <variables>
            {{ 'id': '123', 'description': 'This is a test' }}
            </variables>

            Output:

            <output_code>
            return 'Test'
            </output_code>

            Example 2:

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

            <output_code>
            import random

            return {{
                'description': 'Tic Tac Toe is a game that consists of a 3x3 grid. Players take turns marking the spaces in the grid with X or O. The player who succeeds in placing three of their marks in a horizontal, vertical, or diagonal row is the winner.',
                'players_count': 2,
                'starting_player': random.choice(['X', 'O']),
            }}
            </output_code>

            Example 3:

            <input_code>
            prices = [{{ 'product_id': 1, 'price': 100 }}, {{ 'product_id': 2, 'price': 200 }}, {{ 'product_id': 3, 'price': 300 }}]
            total = smart_call()
            </input_code>

            <variables>
            {{ 'prices': [{{ 'product_id': 1, 'price': 100 }}, {{ 'product_id': 2, 'price': 200 }}, {{ 'product_id': 3, 'price': 300 }}] }}
            </variables>

            Output:

            <output_code>
            return reduce(lambda total, price: total + price['price'], prices, 0)
            </output_code>


            Now, you will receive the actual code where 'smart_call' is invoked:

            <input_code>
            {call_data.code}
            </input_code>

            These are the variables available within the scope of 'smart_call':

            <variables>
            {call_data.variables}
            </variables>

            Return the code that will be returned by the 'smart_call' function, between <output_code> and </output_code>, and nothing else."""
        )

        return {
            "role": "user",
            "content": prompt,
        }
