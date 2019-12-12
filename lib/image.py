import argparse
import time

from .translator import translate as _

def load_image_parser():
  parser = argparse.ArgumentParser(description = _("app.cmd.image.description"))
  subparsers = parser.add_subparsers(dest="subcommand")

  parser_export = subparsers.add_parser('export', help=_("app.cmd.image.export"))
  parser_export.add_argument("alignment", default='align', type=str, choices=['align','super', 'cealign'], help=_("app.cmd.image.alignment"))
  
  parser_show = subparsers.add_parser('view', help=_("app.cmd.image.view"))

  return parser


def image_command(handler, state, printer, args):
  instancer = {
    'view'   : View,
    'export' : Export
  }

  instance = instancer[args.subcommand](handler, state, printer, args)
  instance.do()


class Image:
  def __init__(self, handler, state, printer, args):
    self.handler  = handler
    self.state    = state
    self.printer  = printer
    self.args     = args
    

  def do(self):
    self._do()

  def _do(self):
    pass


class View(Image):
  def __init__(self, handler, state, printer, args):
    super().__init__(handler, state, printer, args)

  def _do(self):
    log = self.printer.log
    if self.state.source_protein_filename and self.state.mutated_protein_filename and self.state.both_proteins_filename:
      log(f'{_("app.guide.image.visualize.header")}:')
      url = 'localhost'
      log(f' * {_("app.guide.image.visualize.source")  } : http://{url}:8080/{self.state.source_protein_filename}.png') 
      log(f' * {_("app.guide.image.visualize.mutated") } : http://{url}:8080/{self.state.mutated_protein_filename}.png') 
      log(f' * {_("app.guide.image.visualize.both")    } : http://{url}:8080/{self.state.both_proteins_filename}.png') 

    else :
      log(_("app.error.image.cant_visualize"))

class Export(Image):
  def __init__(self, handler, state, printer, args):
    super().__init__(handler, state, printer, args)
    image_folders = 'images'
    state.source_protein_filename  = f'{image_folders}/source_protein'
    state.both_proteins_filename   = f'{image_folders}/both_proteins_aligned_{self.args.alignment}'
    state.mutated_protein_filename = f'{image_folders}/mutated_protein'

  def _get_command(self):
    source_protein_sequence = self.state.source_protein.seq
    mutated_protein_sequence = self.state.mutation_protein
    (width, height, dpi) = 4800, 4800, 2000

    return f"pymol -Qcd 'fab {source_protein_sequence}; fab {mutated_protein_sequence}; super obj01, obj02; show sticks, all; disable obj02; zoom; png {self.state.source_protein_filename}, width={width}, height={height}, dpi={dpi}, ray=1; enable obj02; disable obj01; zoom; png {self.state.mutated_protein_filename}, width={width}, height={height} , dpi={dpi}, ray=1; enable obj01; zoom; png {self.state.both_proteins_filename}, width={width}, height={height} , dpi={dpi}, ray=1'"

  def _do(self):
    log = self.printer.log
    if self.state.source_protein and self.state.mutation_protein :
      command = self._get_command()
      self.printer.debug(command)
      self.handler.do_shell(command)
    else : 
      log(_("app.error.image.cant_export"))
    