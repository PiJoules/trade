#!/usr/bin/env bash

# Required args
name=""
strategies_dir="strategies"

print_usage(){
    echo "Usage: $0 -n [-s]"
    echo "Arguments:"
    echo " -n, --name Strategy name."
    echo " -s, --strategies_dir Directory to place this strategy."
    exit 0
}

# Parse cmd line args
while [[ $# > 0 ]]; do
    key="$1"
    case $key in
        -n|--name)
            name="$2"
            shift
            ;;
        -s|--strategies_dir)
            strategies_dir="$2"
            shift
            ;;
        -h|--help)
            print_usage
            exit 0
            ;;
        *)
            echo "Unknown arg: $key"
            exit 1
            ;;
    esac
    shift
done

# Check args
if [ -z $name ]; then
    echo "--name must be provided\n"
    print_usage
    exit 1
fi

# Make dirs
mkdir "$strategies_dir/$name"
mkdir "$strategies_dir/$name/scripts"
mkdir "$strategies_dir/$name/tests"
mkdir "$strategies_dir/$name/tests/expected_outputs"
mkdir "$strategies_dir/$name/tests/inputs"

# Make files
touch "$strategies_dir/$name/__init__.py"
touch "$strategies_dir/$name/scripts/__init__.py"
touch "$strategies_dir/$name/tests/__init__.py"

# Copy and fill templates
cp templates/strategy.py "$strategies_dir/$name/strategy.py"
cp templates/backtest.py "$strategies_dir/$name/scripts/backtest.py"
cp templates/backtest.py "$strategies_dir/$name/scripts/ideal.py"
sed "s/{{name}}/$name/g" templates/setup.py > "$strategies_dir/$name/setup.py"
sed "s/{{name}}/$name/g" templates/test_output.py > "$strategies_dir/$name/tests/test_output.py"

