import argparse
from Bio import SeqIO
from Bio.Alphabet import IUPAC

from .translator import translate as _

def load_fasta_parser():
  load_fasta_parser = argparse.ArgumentParser(description=_("app.cmd.fasta.description"))
  load_fasta_parser.add_argument("-n", type=int, default=0, help=_("app.cmd.fasta.number"))
  load_fasta_parser.add_argument("-f", "--separator", type=str, help=_("app.cmd.fasta.separator"))
  load_fasta_parser.add_argument("-s", "--starting-index", default=None, type=int, help=_("app.cmd.fasta.starting_index"))
  load_fasta_parser.add_argument("-e", "--ending-index", default=None, type=int, help=_("app.cmd.fasta.ending_index"))
  load_fasta_parser.add_argument("fasta", help=_("app.cmd.fasta.fasta"))
  return load_fasta_parser

def load_fasta(input_handler, printer, state, args):
  maybe_id = None
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

    protein = sequence.translate(to_stop = True)

    state.set_up_read_sequence(read_sequence, sequence, protein, starting_index, ending_index, maybe_id)
        
  except:
    printer.error(lambda err : f'{_("app.error.fasta.cant_read")} {args.fasta}, {_("app.error.fasta.cant_read_refer")}: {err[0]} {err[1]}')

def ask_id_info(input_handler, printer, sequence, separator):
  splited = sequence.description.split(separator)
  maybe_id = None
  if len(splited) > 1:
    splited_with_none = splited + [_("app.guide.fasta.none_of_above")]
    answer = None
    options = [i+1 for i in range(len(splited)+1) ]
    while answer not in options:
      printer.log(_("app.guide.fasta.select"))
      for num, name in enumerate(splited_with_none, start=1):
        printer.log(f'  {num}) {name}')
      answer = int(input_handler.read_input(''))
    try :
      maybe_id = splited[answer-1]
    except:
      pass
  return maybe_id