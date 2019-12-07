import argparse
from Bio import SeqIO
from Bio.Alphabet import IUPAC

def load_fasta_parser():
  load_fasta_parser = argparse.ArgumentParser()
  load_fasta_parser.add_argument("-n", type=int, default=0, help="which sequence from fasta file is the one desired")
  load_fasta_parser.add_argument("-f", "--separator", type=str, help="description separator, if any")
  load_fasta_parser.add_argument("-s", "--starting-index", default=None, type=int, help="subsequence start index")
  load_fasta_parser.add_argument("-e", "--ending-index", default=None, type=int, help="subsequence end index")
  load_fasta_parser.add_argument("fasta", help="fasta file to read from disk")
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
    printer.error(lambda err : f'error reading file {args.fasta}, refer: {err[0]} {err[1]}')

def ask_id_info(input_handler, printer, sequence, separator):
  splited = sequence.description.split(separator)
  maybe_id = None
  if len(splited) > 1:
    splited_with_none = splited + ['LOAD_FASTA.ASK.SEPARATOR_OPTIONS.NONE_OF_THE_ABOVE']
    answer = None
    options = [i+1 for i in range(len(splited)+1) ]
    while answer not in options:
      printer.log('LOAD_FASTA.ASK.SEPARATOR_OPTIONS.PDB')
      for num, name in enumerate(splited_with_none, start=1):
        printer.log(f'  {num}) {name}')
      answer = int(input_handler.read_input(''))
    try :
      maybe_id = splited[answer-1]
    except:
      pass
  return maybe_id