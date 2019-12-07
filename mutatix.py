#!/usr/bin/env python
# coding=utf-8
import cmd2
import cmd2.ansi

from lib import command_load_fasta
from lib import mutations
from lib.state import MutatixState, load_status_parser
from lib.printer import MutatixPrinter

class Mutatix(cmd2.Cmd):
    
  def __init__(self):
    """Initialize the base class as well as this one"""
    shortcuts = self._get_shortcuts()
    super().__init__(shortcuts=shortcuts, persistent_history_file='mutatix_history.dat')
    self.printer = MutatixPrinter(self._out_info, self._out_debug, self._out_error)

    self.prompt = 'MUTATIX > '
    self.debug = True

    self._soft_reset()
    
    # self._init_remove_unwanted_commands()


  def _soft_reset(self):
    self.state = MutatixState(self.printer)
  
  def _get_shortcuts(_):
    return dict({'qq': 'quit', '?': 'help'})

  def set_sequence(self, sequence):
    self.sequence = sequence
  def set_sequence_id(self, id):
    self.sequence_id = id

  def _out_debug(self, message):
    if self.debug : self._print_in_color(message, 'yellow')
  def _out_error(self, message):
    self._print_in_color(message, 'red')
  def _out_info(self, message):
    self._print_in_color(message, 'blue')

  def _print_in_color(self, message, color):
    self.poutput(cmd2.ansi.style(message, fg=color))

  def _init_remove_unwanted_commands(_):
    del cmd2.Cmd.do_edit 
    del cmd2.Cmd.do_run_script 
    del cmd2.Cmd.do_set 
    del cmd2.Cmd.do_run_pyscript 
    del cmd2.Cmd.do_shell 
    del cmd2.Cmd.do_macro

    # prompts and defaults

  # def precmd(self, line):
  #   """Runs just before a command line is parsed, but after the prompt is presented."""
  #   pass

  # def postcmd(self, stop, line):
  #   """Runs right before a command is about to return."""
  #   pass

  @cmd2.with_argparser(load_status_parser())
  def do_status(self, args):
    self.state.report(args)

  def do_reset(self, _):
    """ wipe out all stored info in mutatix status """
    self._soft_reset()

  @cmd2.with_argparser(command_load_fasta.load_fasta_parser())
  def do_load_fasta(self, args):
    """ load fasta file for further analysis"""
    command_load_fasta.load_fasta(self, self.printer, self.state, args)
  
  @cmd2.with_argparser(mutations.load_mutation_parser())
  def do_mutate(self, args):
    """ mutate loaded sequence following one of the available strategies"""
    mutations.mutate(self.state, self.printer, args)
    


if __name__ == '__main__':
  import sys  
  # Create an instance of the cmd derived class and enter the REPL with cmdloop().
  mutatix = Mutatix()
  sys_exit_code = mutatix.cmdloop()
  print('Exiting with code: {!r}'.format(sys_exit_code))
  sys.exit(sys_exit_code)