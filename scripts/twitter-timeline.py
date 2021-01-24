#!/usr/bin/env python3


import argparse
import logging
import os
import time

import twint
import twint.tweet
import twint.storage.write


def init_log():
    logging.basicConfig(format='[%(levelname)s] %(asctime)s %(filename)s:%(lineno)s %(message)s', level=logging.INFO)


def save_if_not_exists(out_dir, tweet: twint.tweet.tweet):
    dir_name = os.path.join(out_dir, tweet.username, tweet.datestamp)
    file_name = '%s %s.json' % (tweet.datestamp, tweet.id)
    file_path = os.path.join(dir_name, file_name)

    logging.info('saving tweet[%s] into %s', tweet.id, file_path)

    if os.path.exists(file_path):
        logging.info('tweet[%s] already exists in %s, skip', tweet.id, file_path)
        return
    os.makedirs(dir_name, exist_ok=True)
    twint.storage.write.Json(tweet, twint.Config(Output=file_path))


def run(args):
    c = twint.Config(Username=args.username, Store_object=True, Hide_output=True, Limit=args.limit)

    while True:
        tweets = []
        c.Store_object_tweets_list = tweets
        twint.run.Profile(c)
        logging.info("pulled %d tweets", len(tweets))

        for tweet in tweets:
            save_if_not_exists(args.output, tweet)

        logging.info('sleep for %s seconds', args.sleepseconds)
        time.sleep(args.sleepseconds)


if __name__ == '__main__':
    init_log()

    parser = argparse.ArgumentParser(description='Get timeline from Twitter.')
    parser.add_argument('--username', dest='username', required=True, action='store', type=str, help='username')
    parser.add_argument('--limit', dest='limit', default=30, action='store', type=int, help='limit')
    parser.add_argument('--sleepseconds', dest='sleepseconds', default=30, action='store', type=int,
                        help='time for sleep between each pull')
    parser.add_argument('--output', dest='output', default=os.getcwd(), action='store', type=str,
                        help='output directory')
    args = parser.parse_args()

    logging.info('argument: username is %s, output is %s, limit is %s, sleepseconds is %s', args.username, args.output,
                 args.limit, args.sleepseconds)

    run(args)
