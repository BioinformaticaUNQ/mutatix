import argparse
from random import random, choice, seed
from Bio.Seq import Seq 
from Bio.Alphabet import IUPAC
from Bio import pairwise2
from Bio.pairwise2 import format_alignment

from .translator import translate as _

def load_mutation_parser():
  mutation_parser = argparse.ArgumentParser(description=_("app.cmd.mutate.description"))
  mutation_parser.add_argument("-i", "--iterations",type=int, default=1, help=_("app.cmd.mutate.iterations"))
  mutation_parser.add_argument("-s", "--score",type=int, default=10, help=_("app.cmd.mutate.score"))
  mutation_parser.add_argument("-p", "--probability", default=0.2, type=float, help=_("app.cmd.mutate.probability"))
  mutation_parser.add_argument("-m", "--model", default='JukesCantor', type=str, choices=['JukesCantor'], help=_("app.cmd.mutate.model"))  
  mutation_parser.add_argument("-c", "--stop-codon", default='False', type=bool, help=_("app.cmd.mutate.stop_codon"))  
  return mutation_parser

def mutate(state, printer, args):

  if state.can_mutate():
    models = { 
      'JukesCantor' : lambda args, sequence: JukesCantor(sequence, args.probability),
      'Kimura80' : lambda args : None 
    }

    score = args.score
    obtained_score = 0

    while obtained_score < score:

      original_sequence = state.source_sequence
      model = models[args.model](args, original_sequence)
      mutation_sequence = model.mutate(args.iterations)

      mutation_protein = mutation_sequence.translate(to_stop = args.stop_codon)

      alignment = pairwise2.align.globalxx(state.source_protein.seq, mutation_protein, one_alignment_only = True)[0]

      obtained_score = alignment[2]

    state.mutation_protein = mutation_protein
    state.mutation_sequence = mutation_sequence
    state.alignment = alignment
    # printer.debug(f' original sequence:\n {original_sequence.seq}\n mutated sequence:\n {mutation_sequence}')
    printer.debug(f'{format_alignment(*alignment)}')
    
  else : 
    printer.log(_("app.error.mutate.cant_mutate"))

class MutationModel():
  def __init__(self,sequence):
    self.sequence = sequence
    self.mutated_sequence = None
    self.purines = ['a','g']
    self.pyrimidines = ['c', 't']
    self.nitrogenous_bases = self.purines + self.pyrimidines

  def _mutate_(self, iterations):
    pass

  def mutate(self, iterations):
    return self._mutate_(iterations)

class JukesCantor(MutationModel):  
  def __init__(self, sequence, probability):
    super().__init__(sequence)
    self.probability = probability

  def _mutate_(self, iterations):
    seed()
    sequence = self.sequence
    for iteration in range(iterations):
      mutation_chain = [ i if random() > self.probability else choice(self.nitrogenous_bases) for i in sequence]
      sequence = Seq(''.join(mutation_chain), IUPAC.unambiguous_dna)
    return sequence


class Kimura(MutationModel):
  def __init__(self, sequence):
    super().__init__(sequence)
