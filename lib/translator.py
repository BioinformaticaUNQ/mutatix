import os
from i18n.translator import t 
from i18n import config
from i18n import resource_loader


def translate(string):
  resource_loader.init_loaders()
  config.set('load_path', ['/usr/src/locale'])
  locale = 'en'
  try :
    locale = os.environ['MUTATIX_LOCALE']
  except : 
    pass
  config.set('locale', locale)
  return t(string)
