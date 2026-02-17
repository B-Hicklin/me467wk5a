from hazardous_warehouse_env import HazardousWarehouseEnv
from hazardous_warehouse_viz import configure_rn_example_layout
from warehouse_kb_agent import WarehouseKBAgent
env = HazardousWarehouseEnv(seed=0)
configure_rn_example_layout(env)
print("True state (hidden from agent):")
print(env.render(reveal=True))
agent = WarehouseKBAgent(env)
agent.run(verbose=True)