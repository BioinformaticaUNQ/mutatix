import argparse
from Bio import SeqIO
from Bio.Alphabet import IUPAC

import requests
import re

from .translator import translate as _

def load_fasta_parser():
  load_fasta_parser = argparse.ArgumentParser(description=_("app.cmd.fasta.description"))
  load_fasta_parser.add_argument("-n", type=int, default=0, help=_("app.cmd.fasta.number"))
  load_fasta_parser.add_argument("-f", "--separator", type=str, help=_("app.cmd.fasta.separator"))
  load_fasta_parser.add_argument("-s", "--starting-index", default=None, type=int, help=_("app.cmd.fasta.starting_index"))
  load_fasta_parser.add_argument("-e", "--ending-index", default=None, type=int, help=_("app.cmd.fasta.ending_index"))
  load_fasta_parser.add_argument("fasta", help=_("app.cmd.fasta.fasta"))
  return load_fasta_parser

def load_fasta(handler, input_handler, printer, state, args):
  maybe_id = None
  maybe_pdb_id = None
  try:

    read_sequence = list(SeqIO.parse(args.fasta, "fasta", alphabet=IUPAC.unambiguous_dna))[args.n]
    starting_index = 0
    ending_index = len(read_sequence)

    if args.starting_index : 
      starting_index = args.starting_index
    if args.ending_index : 
      ending_index = args.ending_index

    sequence = read_sequence[starting_index-1:ending_index]
    
    if args.separator: 
      maybe_id = ask_id_info(input_handler, printer, read_sequence, args.separator)
      maybe_pdb_id = lookup_id_pdb_info(maybe_id, input_handler, printer)


    protein = sequence.translate(to_stop = True)

    state.set_up_read_sequence(read_sequence, sequence, protein, starting_index, ending_index, maybe_id, maybe_pdb_id)
        
  except:
    printer.error(lambda err : f'{_("app.error.fasta.cant_read")} {args.fasta}, {_("app.error.fasta.cant_read_refer")}: {err[0]} {err[1]}')

def ask_id_info(input_handler, printer, sequence, separator):
  options = [i for i in sequence.description.split(separator) if i != '' ]
  return input_for_list(input_handler, printer, options, _("app.guide.fasta.select"))

def lookup_id_pdb_info(maybe_id, input_handler, printer):
  selected = None
  if maybe_id:
    printer.log(_("app.guide.id_lookup.start"))
    response = requests.get(f'https://www.uniprot.org/uniprot/?query={maybe_id}&format=tab&columns=database%28PDB%29')
    if response.status_code == 200:
      match = re.search('((\w|\d)+\;)+', response.text)[0]
      options = [i for i in match.split(';') if i != '']
      printer.debug(options)
      selected = input_for_list(input_handler, printer, options, _("app.guide.id_lookup.found_select"))
      printer.debug(selected)
  return selected


def input_for_list(input_handler, printer, list_options, header, text, include_none = True):
  options_number = [i+1 for i in range(len(list_options) + (1 if include_none else 0))]
  options_show = list_options + ([_("app.guide.fasta.none_of_above")] if include_none else [] )
  iterator = zip(options_number, options_show)
  answer = None
  selected = None
  while answer not in options_number:
    printer.log(text)
    for num, name in iterator:
      printer.log(f' {num}) {name}')
    answer = int(input_handler.read_input(''))
  try :
    selected = list_options[answer-1]
  except:
    pass
  return selected
