import sys
import argparse

def load_status_parser():
  status_parser = argparse.ArgumentParser()
  status_parser.add_argument("mode", type=str, choices=['simple','all', 'proteins', 'sequences'], help="what to report status about")  
  return status_parser


class MutatixState() :
  def __init__(self,  printer):
    self.printer = printer
    self.read_sequence = None
    self.start_end_sequence = None
    self.source_sequence = None
    self.source_protein = None
    self.mutation_sequence = None
    self.mutation_protein = None
    self.source_sequence_id = None
    self.source_protein_filename = None
    self.both_proteins_filename = None
    self.mutated_protein_filename = None

  def report(self, args):
    log = self.printer.log
    callback = {
      'proteins' : self._proteins_report
    }

    log(f'############################### status report: {args.mode}  #######################################################################')
    # if self.source_sequence :    
    #   log(f'source sequence, from: {self.start_end_sequence} : {self.source_sequence}')
    #   log('******************************************************************************************************')
    # if self.source_sequence_id : 
    #   log(f'registered id : {self.source_sequence_id}')
    #   log('******************************************************************************************************')
    # if self.source_protein : 
    #   log(f'source sequence translated to protein : {self.source_protein}')
    #   log('******************************************************************************************************')
    callback[args.mode](args)

    log('####################################################################################################################################')

  def _proteins_report(self, agrs):
    log = self.printer.log
    if self.source_protein :
      log(f'source protein : {self.source_protein.seq}')
    if self.mutation_protein :
      log(f'mutation_protein : {self.mutation_protein}')


  def set_up_read_sequence(self, read, sequence, protein, start,end, maybe_id):
    self.read_sequence = read
    self.source_sequence = sequence
    self.start_end_sequence = (start, end)
    self.source_sequence_id = maybe_id
    self.source_protein = protein
    # self.printer.debug(f'{self.source_sequence}, {self.start_end_sequence}')

  def can_mutate(self):
    return self.source_sequence and self.source_protein
