My Pythony Puppet Ruby vim IDE 
##############################

:date: 2014-09-13
:comments: true
:slug: my-pythony-puppet-ruby-ide
:tags: devops, vim, python, puppet
:summary: Using Vi for Python and Puppet development

.. figure:: {filename}/images/0k24Ambl.png
    :align: right
    :width: 400px

Despite my penchant for tools written in Ruby (Puppet, Gitlab, Jekyll/Octopress
etc) I do not actually like Ruby. I am more of a Python guy. I also like
Vim, so whenever I use a GUI IDE I end up with something littered with
``:w`` and ``ZZ``. (

Despite my pythonic leanings, I also need something that can handle Ruby
and Puppet's DSL. To which end, this is a bit of a mixture. Fortunately,
nothing in either world really contradicts the other, so it works pretty
nicely.

First, the basic environments. Git is needed everywhere, plus I need to
isolate the environments of the various projects.

::

    sudo apt install git python python-dev python-virtualenv virtualenvwrapper curl libxml2-dev libxslt-dev zlib1g-dev ruby-dev
    echo "pip install pyflakes" >> ~/.virtualenvs/postmkvirtualenv
    curl -sSL https://get.rvm.io | bash -s stable --ruby

Now we have Git, Virtualenv (and virtualenvwrapper) and RVM installed.

Vim
===

This the core of everything. I use quite a few plugins:

-  `Autoclose <https://github.com/andrewle/vim-autoclose>`__: Inserts
   matching bracket, paren, brace or quote
-  `Colour Sampler
   Pack <https://github.com/vim-scripts/Colour-Sampler-Pack>`__: Gives
   me a nice colour scheme
-  `Gundo <https://github.com/sjl/gundo.vim>`__: Visualise the undo tree
-  `Lusty <https://github.com/sjbach/lusty>`__: Manage files within Vim
-  `PEP-8 <https://github.com/cburroughs/pep8>`__: Validate the style of
   Python files
-  `PyDoc <https://github.com/vim-scripts/pydoc.vim>`__: Python
   documentation view- and search-tool (uses pydoc)
-  `Pathogen <https://github.com/tpope/vim-pathogen>`__: Plugin Manager
-  `Scroll Colours <https://github.com/vim-scripts/ScrollColors>`__:
   Colorsheme Scroller, Chooser, and Browser
-  `Supertab <https://github.com/ervandew/supertab>`__: Tab completion
-  `VirtualEnv <https://github.com/jmcantrell/vim-virtualenv>`__: Works
   with Virtualenvs
-  `Vim Puppet <https://github.com/rodjek/vim-puppet>`__: Puppet
   niceties
-  `Tabular <https://github.com/godlygeek/tabular>`__: Text filtering
   and alignment
-  `Markdown <https://github.com/hallison/vim-markdown>`__: Markdown
   syntax highlighter with snippets support

I keep all this under Git control (available
`here <https://gitlab.chriscowley.me.uk/chriscowleyunix/vim-configuration>`__).
You can just clone my repo and create a symlink for your ``.vimrc``. If
you would rather see what you are doing, then you can replicate my set
up like this:

::

    mkdir -p ${HOME}/.vim/{autoload,bundle}
    cd ${HOME}/.vim/
    git init
    git submodule add https://github.com/andrewle/vim-autoclose.git bundle/vim-autoclose
    git submodule add https://github.com/vim-scripts/Colour-Sampler-Pack.git bundle/colour-sampler-pack
    git submodule add https://github.com/sjl/gundo.vim.git bundle/gundo
    git submodule add https://github.com/sjbach/lusty.git bundle/lusty
    git submodule add https://github.com/cburroughs/pep8.git bundle/pep8
    git submodule add https://github.com/vim-scripts/pydoc.vim.git bundle/pydoc
    git submodule add https://github.com/tpope/vim-pathogen.git bundle/pathogen
    git submodule add https://github.com/vim-scripts/ScrollColors.git bundle/scrollColors
    git submodule add https://github.com/ervandew/supertab.git bundle/supertab
    git submodule add https://github.com/jmcantrell/vim-virtualenv.git bundle/vim-virtualenv
    git submodule add https://github.com/rodjek/vim-puppet.git bundle/puppet
    git submodule add https://github.com/godlygeek/tabular.git bundle/tabular
    git submodule add https://github.com/hallison/vim-markdown.git bundle/markdown
    git submodule init
    git submodule update
    git submodule foreach git submodule init
    git submodule foreach git submodule update
    ln -s ../bundle/pathogen/autoload/pathogen.vim autoload/pathogen.vim
    mv $HOME/.vimrc .
    ln -s '$HOME/.vim/.vimrc' $HOME/.vimrc

Add the following to your ``.vimrc``:

::

    " pathogen
    let g:pathogen_disabled = [ 'pathogen' ]    " don't load self
    call pathogen#infect()                      " load everyhting else
    call pathogen#helptags()                    " load plugin help files
     
    " code folding
    set foldmethod=indent
    set foldlevel=2
    set foldnestmax=4
      
    " indentation
    set autoindent
    set softtabstop=4 shiftwidth=4 expandtab
       
    " visual
    highlight Normal ctermbg=black
    set background=dark
    set cursorline
    set t_Co=256
        
    " syntax highlighting
    syntax on
    filetype on                 " enables filetype detection
    filetype plugin indent on   " enables filetype specific plugins
         
    " colorpack
    colorscheme vibrantink

    " gundo
    nnoremap <F5> :GundoToggle<CR>

    " lusty
    set hidden
    let g:LustyJugglerSuppressRubyWarning = 1"
            
    " pep8
    let g:pep8_map='<leader>8'
             
    " supertab
    au FileType python set omnifunc=pythoncomplete#Complete
    let g:SuperTabDefaultCompletionType = "context"
    set completeopt=menuone,longest,preview

There's quite a lot going on there. Refer to the various plugin docs
linked above to find what it all does. This would be a good moment to
commit all that.

::

    git add .
    git commit -m "Initial commit"

Tmux
====

I use this so I can have a single console window, with multiple panes.
Tmux is configured with the file ``$HOME/.tmux.conf``, mine contains:

::

    set-window-option -g mode-keys vi
    bind h select-pane -L
    bind j select-pane -D
    bind k select-pane -U
    bind l select-pane -R
    unbind -n C-b
    set -g prefix C-a

    # easy-to-remember split pane commands
    bind h split-window -h
    bind v split-window -v
    unbind '"'
    unbind %

    bind -n M-Left select-pane -L
    bind -n M-Right select-pane -R
    bind -n M-Up select-pane -U
    bind -n M-Down select-pane -D
    set-window-option -g window-status-current-bg yellow

    # Just click it
    set-option -g mouse-select-pane on
    set-option -g mouse-select-window on
    set-option -g mouse-resize-pane on
     
    # Scroll your way into copy mode (scrollback buffer)
    # and select text for copying with the mouse
    setw -g mode-mouse on

    set -g set-titles on
    set -g set-titles-string "#T"

Now I can use ``Ctrl+a`` instead of ``Ctrl+b``. You may not need to do
this, but I have little hands.I also change the kes for splitting my
windows (*'h'* horizontally, *v* vertically). I make a few changes from
the defaults:

-  ``Ctrl+a`` instead of ``Ctrl+b`` is my prefix. This matches
   ``screen``, plusI am more comfortable as I have small hands.
-  I can move around panes with either ``vi`` keys, arrows or just with
   the mouse.
-  I change the keys to split windows to ``h`` (horizontal) and ``v``
   (vertical).

This all works pretty well for me, although not perfectly. At the moment
my clipboard gets intercepted by Tmux,which is top of my my list to fix.
