# run with `source activate.sh` to activate the virtual environment
if [ ! -d .venv ]; then
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
fi

source .venv/bin/activate
echo "Using $(which python)"