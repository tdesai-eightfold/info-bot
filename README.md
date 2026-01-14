# Setup
1. Go to cap-server directory
## Install dependencies
  1. `uv add "livekit-agents[silero,turn-detector]~=1.3" "livekit-plugins-noise-cancellation~=0.2" "python-dotenv" "pandas" "flask" "flask_cors" "flask_restx"`
  2. `uv run server.py download-files`
  
# Run the server (console mode)
  `uv run server.py console`
# Run the server (dev mode to use frontend)
  1. `uv run server.py dev` in first terminal
  2. `uv run token-service.py` in another terminal
  3. `lk room create test-room` in third terminal
  4. Open index.html it chrome

# Key Features of voice bot 
This voice bot uses an `EmployeeField` enum to control **who can see which employee details**.
Each field (Email, Phone, Address, Role, Salary) is marked as **restricted or not**.

* If a field is **restricted**, the bot masks it as `********`
* If it’s **not restricted**, the bot reads the actual value

### HR example (needs salary access)
* **HR user** → `salary.restricted = False`
  The bot can respond with the employee’s **actual salary**
* **Non-HR user** → `salary.restricted = True`
  The bot says `********` instead of the salary

The access rules are fully customizable any field can be restricted or opened dynamically based on requirements (such as user role, permissions, or policy).
This allows flexible control over sensitive information without changing the core logic.
