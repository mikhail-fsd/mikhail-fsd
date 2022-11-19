import moex


def create_output_table(df, start_text):
    """prepare output table"""
    if start_text is None:
        out = '```\n'
    else:
        out = start_text

    df.reset_index(inplace=True)
    df_dict = df.to_dict('split')
    
    for value in df_dict['columns']:
        ln = len(value) + 2 # for indent
        out += f'{value: <{ln}}'
    out += '\n'

    for value in df_dict['data']:
        for i, y in enumerate(value):
            ln = len(df_dict['columns'][i]) + 2 # align
            out += f"{y : <{ln}}"
        out += '\n'
    out += '```' # markdowm for monotype
    return out

def base_index():
    df = moex.get_data_dframe()
    out = '```\n' # markdowm for monotype
    out += f"last update: {df.loc[df.index[1], 'weight_update']}\n\n"  # add last date update
    df.drop(columns='weight_update', inplace=True)

    out = create_output_table(df, out)
    return out
 
def shares_price():
    df = moex.get_price_dframe()
    out = '```\n' # markdowm for monotype
    out += f"last update: {df.loc[df.index[1], 'price_update_time']}\n\n"  # add last date update
    df.drop(columns='price_update_time', inplace=True)

    out = create_output_table(df, out)
    return out

def new_user(user_id):
    moex.user_init(user_id=user_id)

def update_goal(user_id, goal):
    moex.update_user_goal(user_id, goal)

def message_passing(messege):
    pass

print(shares_price())

