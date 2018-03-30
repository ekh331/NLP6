#/usr/bin/env python
import os
import time
import datetime

def memoize(f):
    memo = {}
    def _f(*args):
        if args not in memo:
            memo[args] = f(*args)
        return memo[args]
    return _f


@memoize
def results_dir():
    now = datetime.datetime.now()
    return "%02d_%02d_%02d" % (now.hour, now.minute, now.second)
 

# Given data
train = "data/CONLL_train.pos-chunk-name"
dev_pos_chunk = "data/CONLL_dev.pos-chunk"
dev_name = "data/CONLL_dev.name"
test_pos_chunk = "data/CONLL_test.pos-chunk"

# Files to be created
noise = os.path.join(results_dir(), "noise.txt")
train_enhanced = os.path.join(results_dir(), "train_enhanced.txt")
model = os.path.join(results_dir(), "model.txt")
dev_enhanced = os.path.join(results_dir(), "dev_enhanced.txt")
dev_response = os.path.join(results_dir(), "dev_response.txt")
dev_score = os.path.join(results_dir(), "dev_score.txt")
test_enhanced = os.path.join(results_dir(), "test_enhanced.txt")
test_response = os.path.join(results_dir(), "test_response.txt")

# Command string
java = "java -classpath java:java/*"    


def run(cmd):
    #print cmd
    os.system(cmd)
    time.sleep(0.1)


def main():
    # Setup
    rd = results_dir()
    run("mkdir %s" % rd)
    run("cp feature_builder.py %s/feature_builder.py" % (
           rd))

    # Build model
    run("python feature_builder.py --input %s --labels > %s" % (
           train, train_enhanced))
    run("%s MEtrain %s %s" % (
           java, train_enhanced, model))
    
    # Evaluate on dev data
    run("python feature_builder.py --input %s > %s" % (
           dev_pos_chunk, dev_enhanced))
    run("%s MEtag %s %s %s" % (
           java, dev_enhanced, model, dev_response))
    run("python my_scorer.py --actual %s --predicted %s > %s" % (
           dev_name, dev_response, dev_score))
    run("cat %s" % dev_score)

    # Make predictions on test data
    run("python feature_builder.py --input %s > %s" % (
           test_pos_chunk, test_enhanced))
    run("%s MEtag %s %s %s" % (
           java, test_enhanced, model, test_response))


if __name__ == "__main__":
    main()
