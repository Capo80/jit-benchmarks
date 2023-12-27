# TODO need some error checking in here

# prepare test folder
test_folder=$(date +%s)_test
mkdir $test_folder
chown user:user $test_folder

# pwd starts in the jit-bench folder
pushd ../..


# prepare test languages
apt-get update
apt install php-cli
apt install luajit
apt install lua-posix
apt install ruby

# no env :)
pip3 install numpy
pip3 install pandas

############################ sync

# mount module
make EXTRA_CFLAGS=-DKERNEL_SYNC_CHECK=42
insmod hook.ko

# start agent
python3 user/agent.py &
AGENT_PID=$!

#run test
popd
python3 jit_test_fine.py $test_folder/sync.csv
chown user:user $test_folder/sync.csv
pushd ../..

# clean up
kill -9 $AGENT_PID
rmmod hook.ko

############## not sync

# mount module
make
insmod hook.ko

# start agent
python3 user/agent.py &
AGENT_PID=$!

#run test
popd
python3 jit_test_fine.py $test_folder/no_sync.csv
chown user:user $test_folder/no_sync.csv
pushd ../..

# clean up
kill -9 $AGENT_PID
rmmod hook.ko

############## not mod

#run test
popd
python3 jit_test_fine.py $test_folder/no_mod.csv
chown user:user $test_folder/no_mod.csv
pushd ../..

