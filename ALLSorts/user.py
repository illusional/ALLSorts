#=======================================================================================================================
#
#   ALLSorts v2 - Command Line Interface
#   Author: Breon Schmidt
#   License: MIT
#
#   Parse user arguments
#
#=======================================================================================================================

''' --------------------------------------------------------------------------------------------------------------------
Imports
---------------------------------------------------------------------------------------------------------------------'''

''' Internal '''
from ALLSorts.common import message, root_dir

''' External '''
import sys, argparse
import pandas as pd

''' --------------------------------------------------------------------------------------------------------------------
Classes
---------------------------------------------------------------------------------------------------------------------'''

class UserInput:

    def __init__(self):
        if self._is_cli():
            self.cli = True
            self.input = self._get_args()
            self.samples = self.input.samples
            self.labels = self.input.labels if self.input.labels else False
            self.model_dir = str(root_dir())+"/models/allsorts/" if not self.input.model_dir else self.input.model_dir
            self.destination = False if not self.input.destination else self.input.destination
            self.test = self.input.test
            self.train = False if not self.input.train else True
            self.comparison = False if not self.input.comparison else True
            self.n_jobs = 1 if not self.input.njobs else int(self.input.njobs)
            self.verbose = False if not self.input.verbose else True
            self.force = False if not self.input.force else True
            self.cv = 3 if not self.input.cv else int(self.input.cv)
            self.parents = False if not self.input.parents else True
            self._input_checks()
            self._load_samples()
        else:
            self.cli = False

    def _is_cli(self):
        return len(sys.argv) > 1

    def _get_args(self):

        ''' Get arguments and options from CLI '''

        cli = argparse.ArgumentParser(description="ALLSorts CLI")
        cli.add_argument('-samples', '-s',
                         required=True,
                         help=("""Path to samples (rows) x genes (columns) 
                                  csv file representing a raw counts matrix.

                                  Note: hg19 only supported currently, use 
                                  other references at own risk."""))

        cli.add_argument('-labels', '-l',
                         required=False,
                         help=("""(Optional) 
                                  Path to samples true labels. CSV with
                                  samples (rows) x [sample id, label] (cols).

                                  This will enable re-labelling mode.

                                  Note: labels must reflect naming conventions
                                  used within this tool. View the ALLSorts 
                                  GitHub Wiki for further details."""))

        cli.add_argument('-destination', '-d',
                         required=False,
                         help=("""Path to where you want the final
                                  report to be saved."""))

        cli.add_argument('-test', '-t',
                         required=False,
                         action='store_true',
                         help=("""Test will run a simple logistic regression."""))

        cli.add_argument('-train',
                         required=False,
                         action='store_true',
                         help=("""Train a new model. -labels/-l and -samples/-s must be set."""))

        cli.add_argument('-model_dir',
                         required=False,
                         help=("""Directory for a new model. -train -t flag must be set."""))

        cli.add_argument('-njobs', '-j',
                         required=False,
                         help=("""(int, default=1) Will set n_jobs for all Sklearn estimators/transformers."""))

        cli.add_argument('-cv',
                         required=False,
                         help=("""(int, default=3) If training, how many folds in the cross validation?"""))

        cli.add_argument('-verbose', '-v',
                         required=False,
                         action="store_true",
                         help=("""(flag, default=False) Verbose. Print stage progress."""))

        cli.add_argument('-comparison',
                         required=False,
                         action="store_true",
                         help=("""Rebuild comparisons for labelled visualisations."""))

        cli.add_argument('-force', '-f',
                         required=False,
                         action="store_true",
                         help=("""(flag, default=False) Force. Bypass warnings without user confirmation."""))

        cli.add_argument('-parents', '-p',
                         required=False,
                         action="store_true",
                         help=("""Include parent meta-subtypes in predictions. Note: This may remove previously 
                                  unclassified samples."""))

        user_input = cli.parse_args()
        return user_input


    def _input_checks(self):

        if self.train and not (self.labels and self.samples):
            message("Error: if -train is set both -labels/-l, -params/-p, -samples/-s must be also. Exiting.")
            sys.exit()

        if not self.train and not self.destination:
            message("Error: if -train is not set a destination (-d /path/to/output/) is required. Exiting.")
            sys.exit()


    def _load_samples(self):
        if self.samples:
            self.samples = pd.read_csv(self.samples, index_col=0, header=0)

        if self.labels:
            self.labels = pd.read_csv(self.labels, index_col=0, header=None, squeeze=True)
            self.labels.name = "labels"








