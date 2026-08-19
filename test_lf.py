from dotenv import load_dotenv
from langfuse import Langfuse

load_dotenv()
lf = Langfuse()

print("Auth Check:", lf.auth_check())

# Safe method invocation across SDK versions
if hasattr(lf, "trace"):
    lf.trace(name="manual_test_trace", input="hello", output="world")
elif hasattr(lf, "create_trace"):
    lf.create_trace(name="manual_test_trace", input="hello", output="world")
elif hasattr(lf, "start_trace"):
    lf.start_trace(name="manual_test_trace", input="hello", output="world")

lf.flush()
print("Trace Dispatched Successfully!")
