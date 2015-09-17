require 'rubygems'
require 'dream_cheeky'

DreamCheeky::BigRedButton.run do
  push do
    `python printer.py`
  end
end
