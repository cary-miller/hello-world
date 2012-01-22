syntax on

"open file at last position.
au BufWinLeave * mkview
au BufWinEnter * silent loadview



set history=5000		" lines of command line history
highlight Statement ctermfg=DarkGreen



" """""""""""""""" Making Vim a IDE """""""""""""""""""
"of course this could be set to something else as well
" Not only that.  It could be set to diff program for diff file type.
set keywordprg=texdoc
set keywordprg=pydoc
" How to call keyword program?
" K


" http://blog.dispatched.ch/2009/05/24/vim-as-python-ide/
" autocompletion
autocmd FileType python set omnifunc=pythoncomplete#Complete
" if autocompletion does not work with this^ then there is a plugin
" required.  Link at the blog post above.
" Is this supposed to be two lines? ^
" I can get it to work by saying :set omnifunc=pythoncomplete#Complete
" for each individual file
" Seems to recognize only var names not python keywords.

" Python ..................................................
python << EOF
import vim
cb = vim.current.buffer
name = cb.name
text_width = vim.eval("&tw")

from socket import socket, AF_INET, SOCK_STREAM
def _send(message):
    to_python = socket(AF_INET, SOCK_STREAM)
    host=''
    port=2001
    to_python.connect((host,port))
    to_python.send(message)

def send(lines): _send('\n'.join(lines))

def send_r(): send(vim.current.range)
def send_line(): send(vim.current.line.strip())


EOF
" Python ..................................................

" re that old IPC bugaboo.  See bash:coproc?


" TODO: see SuperTab plugin for autocompletion
" also see http://aymanh.com/a-collection-of-vim-tips

" ^n word completion!  No nothing required.


" Buffer navigation with control-Tab
nnoremap <C-Tab> :bnext
nnoremap <C-S-Tab> :bprevious<CR>
" fails




"erlanger response to post above
"My favorite Vim customization for Python coding:
":nnoremap :w !python
"You put this in the ftplugin file(s).
" ft: File Type


" TaskList plugin
"   Organizes TODO FIXME etc statements.


" """""""""""""""" Here is amazing stuff """""""""""""""""""
" The vim Taglist plugin transforms vim to a source code BROWSER.
" cd ~/.vim
" wget -O taglist.zip http://www.vim.org/scripts/download_script.php?src_id=7701
" unzip taglist.zip
filetype plugin on
" error
" http://www.thegeekstuff.com/2009/04/ctags-taglist-vi-vim-editor-as-sourece-code-browser/
" Taglist: Failed to generate tags for 
" Fixed: by changing from ctags to Exuberant ctags
" p:  show def but stay here
" s: sort
" b: delete all tags for this file
" +-*= : folds. Whatever those are.
" backspace / tab : next/prev file
" x max/minimizes TagList
" 
let Tlist_Exit_OnlyWindow = 1
let Tlist_Highlight_Tag_On_BufEnter = 1
let Tlist_Display_Prototype = 0

nnoremap <silent> <F7> :TlistUpdate <CR>
nnoremap <silent> <F8> :TlistToggle <CR>
" http://vim-taglist.sourceforge.net/manual.html#taglist-using

nnoremap <silent> <F9> :TaskList <CR>

" Install Tasklist plugin
" wget -O taglist.zip http://www.vim.org/scripts/download_script.php?src_id=2607


" Also there is cscope, also incredibly useful
" http://cscope.sourceforge.net/cscope_vim_tutorial.html
" 

" """"""""""""""""""""""" Block comment """"""""""""""""""""
" *blockwise* visual mode: C-V
" C-V I text-to-prepend <Esc>
" or of course
" V :s/^/# /
" Or use marks `a, `e to operate on huge sections.
" :`a,`e s/^/# /
" : 1,$ s/^/# /   $ is last line



" ReStructuredText ab
map mm i>>> <Esc>0j
map nn i... <Esc>0j



ab #! #!/usr/bin/env
ab #n # NOTE:
" django abbrev
ab bl <Esc>bi{% block <Esc>ea %}{% endblock %}<Esc>h%i
" HTML abbrev
ab tg <Esc>xbdwi<></><Esc>bplllpbhhi

" MySQL
ab mys MySQLdb


map -- i#!/usr/bin/env 
map td i# TODO: 

set clipboard=autoselect
set printoptions=paper:letter
set nocompatible
set cpo=B
set wrapmargin=8
set autoindent
set sw=4
set tabstop=4
set et
" expandtabs
set incsearch
set nohls
" turn off annoying search highlighting
set autowrite
" saves the current file when you say :e foo

"set mouse=a
" NOT SURE IF THIS IS REALLY VERY USEFUL
"set mouse=""
" turns off the mouse and allows pasting from outside vim


set showmatch
" show matching () [] {}


imap <C-a> <Esc>I
imap <C-e> <Esc>A

map! <xHome> <Home>
map! <xEnd> <End>
map! <S-xF4> <S-F4>
map! <S-xF3> <S-F3>
map! <S-xF2> <S-F2>
map! <S-xF1> <S-F1>
map! <xF4> <F4>
map! <xF3> <F3>
map! <xF2> <F2>
map! <xF1> <F1>

map <xHome> <Home>
map <xEnd> <End>
map <S-xF4> <S-F4>
map <S-xF3> <S-F3>
map <S-xF2> <S-F2>
map <S-xF1> <S-F1>
map <xF4> <F4>
map <xF3> <F3>
map <xF2> <F2>
map <xF1> <F1>

