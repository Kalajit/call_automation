import redis

REDIS_URL = "redis://default:<PASSWORD>@red-d3ajjci4d50c73dc0gg0.upstash.io:6379"  # Example

r = redis.Redis.from_url(REDIS_URL)

agent_type = r.get("outbound_1758878153525_-3204877647059288407:agent_type")
initial_message = r.get("CA8e9562fc115fe41eaa9052134b23f3a0:initial_message")

print("agent_type:", agent_type.decode() if agent_type else None)
print("initial_message:", initial_message.decode() if initial_message else None)
