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
  mutation_parser.add_argument("-m", "--model", default='JukesCantor', type=str, choices=['JukesCantor', 'manual'], help=_("app.cmd.mutate.model"))  
  mutation_parser.add_argument("-c", "--stop-codon", default='False', type=bool, help=_("app.cmd.mutate.stop_codon"))  
  return mutation_parser

def mutate(handler, state, printer, args):

  if state.can_mutate():
    models = { 
      'JukesCantor' : lambda args, sequence: JukesCantor(sequence, args.probability, args.iterations),
      'manual' : lambda _, sequence : Manual(sequence, handler),
      'Kimura80' : lambda args : None 
    }



    score = args.score
    obtained_score = 0

    while obtained_score < score:

      original_sequence = state.source_sequence
      model = models[args.model](args, original_sequence)
      mutation_sequence = model.mutate()

      mutation_protein = mutation_sequence.translate(to_stop = args.stop_codon)

      alignment = pairwise2.align.globalxx(state.source_protein.seq, mutation_protein, one_alignment_only = True)[0]

      obtained_score = alignment[2] if args.model != 'manual' else args.score

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

  def _mutate_(self):
    pass

  def mutate(self):
    return self._mutate_()

class JukesCantor(MutationModel):  
  def __init__(self, sequence, probability, iterations):
    super().__init__(sequence)
    self.probability = probability
    self.iterations = iterations

  def _mutate_(self):
    seed()
    sequence = self.sequence
    for iteration in range(self.iterations):
      mutation_chain = [ i if random() > self.probability else choice(self.nitrogenous_bases) for i in sequence]
      sequence = Seq(''.join(mutation_chain), IUPAC.unambiguous_dna)
    return sequence


class Kimura(MutationModel):
  def __init__(self, sequence):
    super().__init__(sequence)

class Manual(MutationModel):
  def __init__(self, sequence, handler):
    super().__init__(sequence)
    self.handler = handler

  def _mutate_(self):
    read = ''
    print(self.sequence.seq.__str__())
    with open('/tmp/mutation_manual', 'w') as file:
      file.write(self.sequence.seq.__str__())
    self.handler.do_shell('vim /tmp/mutation_manual')
    with open('/tmp/mutation_manual') as file:
      read = file.read()
    sequence = Seq(read, IUPAC.unambiguous_dna)
    return sequence
