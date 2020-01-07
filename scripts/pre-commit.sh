#!C:/PROGRA~1/Git/bin/sh.exe
echo "Running pre-commit hook"
cd ../
python checkGrammarTreeCreation.py --test
if [ $? -ne 0 ]
then
    echo "One of the tests failed! Pass them before commit"
    exit 1
fi

echo "Tests passed!"
