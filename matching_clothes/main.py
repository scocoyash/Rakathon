import os
from operator import itemgetter
import pickle

import indicoio
from indicoio.custom import Collection
indicoio.config.api_key = 'b1885d01b85e70a8f36452cbc4e66a6a'

def generate_training_data(fname):
    with open(fname, "rb") as f:
        for line in f:
            shirt, targets = line.split(":")
            shirt_path = "training_shirts_men/{image}.jpg".format(
                image=shirt.strip()
            )
            shirt_path = os.path.abspath(shirt_path)

            # parse out the list of targets
            target_list = targets.strip()[1:-1].split(",")
            labels = map(lambda target: "label" + target.strip(), target_list)
            yield [ (shirt_path, label) for label in labels]
    raise StopIteration


if __name__ == "__main__":
    collection = Collection("clothes_collection_1")

    # Clear any previous changes
    try:
        collection.clear()
    except:
        pass

    train = generate_training_data("clothes_match_labeled_data_1.txt")

    total = 0
    for samples in train:
        print "Adding {num} samples to collection".format(num=len(samples))
        collection.add_data(samples)
        total += len(samples)
        print "Added {total} samples to collection thus far".format(total=total)

    collection.train()
    print "Training..."
    collection.wait()
    file = open('../predict_matching', 'wb')
    pickle.dump(collection, file)
    file.close()
    
    sort_key = itemgetter(1)
    print sorted(collection.predict("test_shirts/1.jpg").items(), key=sort_key)
    print sorted(collection.predict("test_shirts/2.jpg").items(), key=sort_key)
    print sorted(collection.predict("test_shirts/3.jpg").items(), key=sort_key)
    print sorted(collection.predict("test_shirts/4.jpg").items(), key=sort_key)
    print sorted(collection.predict("test_shirts/5.jpg").items(), key=sort_key)
