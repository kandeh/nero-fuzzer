What is Nero?
------
Nero is an open source HTTP API fuzzer aiming to be easy to use and extend. Currently, Nero's main focus is to find and report server errors.

Hence Nero is modular, it is easy to extend it. Nero is powered by some small modules at the moment but it will have many powerful modules very soon.

Currently, Nero is extremely under development and any contribution is appreciated.

Run Nero
------
First of all, you need to run your HTTP server. Let's assume your HTTP server is already up and running and it is accessible on http://localhost:8000/.


Install Nero requirements:
```
pip install requirements.txt
```

Set Nero's target:
```
export NERO_TARGET=http://localhost:8000
```

It is recommended (but not required) to help Nero by giving a text file containing some valid secrets, usernames, uuids, urls, etc. You need to put each one in a separate line. For example:
```
admin@test.com
/search
/api/v1/login
123456
```

Put all your helps in a file and give it to Nero:
```
export NERO_DICT_PATH=/path/to/file
```

Now you can run Nero:
```
bash run_nero.bash
```

Open Nero's web UI and enjoy:
```
http://localhost:5000/
```
