import taipy as tp
import pandas as pd
from taipy import Config
from taipy.gui import Gui, Markdown, notify

Config.configure_global_app(clean_entities_enabled=True)
tp.clean_all_entities()

input_text_cfg = Config.configure_data_node(id="input_text")
text_length_cfg = Config.configure_data_node(id="text_length")

count_characters_cfg = Config.configure_task(id="count_characters", function=len, input=input_text_cfg, output=text_length_cfg)

scenario_cfg = Config.configure_scenario_from_tasks(id="count_characters", task_configs=[count_characters_cfg])

scenario_list = tp.get_scenarios()
input_text = ""
main_md = Markdown("""
# Taipy Character Counter

Enter Text:

<|{input_text}|input|>

<|Submit|button|on_action=submit|>

----------

Past Results:

<|{create_results_table(scenario_list)}|table|width=fit-content|>
""")

def submit(state):
    scenario = tp.create_scenario(scenario_cfg)
    scenario.input_text.write(state.input_text)
    
    state.input_text = ""
    
    tp.submit(scenario, wait=True)
    notify(state, "S", "Submitted!")

    state.scenario_list = tp.get_scenarios()



def create_results_table(scenario_list):
    table = [(s.id, s.input_text.read(), s.text_length.read()) for s in scenario_list]
    df = pd.DataFrame(table, columns=["id", "input_text", "text_length"])
    print(df)
    return df

tp.Core().run()
gui = Gui(main_md)
gui.run(run_browser=False)
