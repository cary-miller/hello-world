from xml_from_data import tag, concat, tag_gen, head_tail

for name in '''html head body title script style h1 p
    foo bar bat
    table tr td th
    form select option input button
    div pre hr
    g circle svg text
    '''.split():

    exec(tag_gen %locals())


# ################### Composite tag functions ################### #

op_tag = lambda name, val: tag('option', val, [('value', val), ('name', name)])
op_tag_list = lambda name, val_list: '\n'.join([ op_tag(name, v) for v in val_list])

checkbox = lambda name, val: tag('input', val,  attributes=[ 
    ('type', "checkbox"), ('class', name), ('value', val)])

checkbox_list = lambda name, val_list: '\n'.join([
    checkbox(name, v) for v in val_list])    

radio = lambda name, val: tag('input', val,  attributes=[ 
    ('type', "radio"), ('name', name), ('value', val)])

radio_list = lambda name, val_list: '\n'.join([
    radio(name, v) for v in val_list])    


with open('data_structures.js') as fh: dscode = fh.read()
with open('data_viewer.js') as fh: jscode = fh.read()
with open('basic.css') as fh: csscode = fh.read()

head = head( concat(
    title('proto'),
    script(' ', 
        ["type","text/javascript"],
        ["src","http://code.jquery.com/jquery-2.0.2.js"]),

#    script(' ', 
#        ["src","http://d3js.org/d3.v3.min.js"],
#        ["charset","utf-8"],
#        ),

    script(dscode,  ["type","text/javascript"]),
    script(jscode,  ["type","text/javascript"]),
    style(csscode,  ["type","text/css"]),
))



users = 'smith jones'.split()
casenames = 'case1 case2 case3 case4 case5'.split() 
datasets = 'fred1 fred2 fred3'.split()
user_options = op_tag_list('user', users)
case_options = op_tag_list('case', casenames)
dataset_options = op_tag_list('data set', datasets)


#columns = 'ticket date docid xxxid'.split()
#column_checks = checkbox_list('col_check', columns) # for column subsetting.
#column_radio = radio_list('col_radio', columns) # for filtering on column values
column_radio = radio('col_radio', 'any') # for filtering on column values



table1 = table(concat(

#    tr(concat(
#        td('Case'),
#        td(select(case_options, ["id","da_case"])),
#        td(''),
#        )) ,
#
#    tr(concat(
#        td('User'),
#        td(select(user_options, ["id","da_user"])),
#        td(''),
#        )) ,
#
#    tr(concat(
#        td('Columns'),
#        td(select(column_options, [["id","da_cols"]])),
#        td(''),
#        )) ,

    tr(concat(
        td('Data'),
        td(select(dataset_options, ["id","data_options"])),
        td(''),
        )) ,


    tr(concat(
        td(''),
        td(input('', ["type","submit"], ["value","Go!"],
            ["id","submitA"])),
        td(''),
        )) ,

        )) # end table1


sort_controls = concat(p('Sort/Filter Controls'),
    table(concat(

    tr(concat(
        td('Chop head:'),
        td(),
        td(input('', ['type', 'text'], ['id', 'n_chop'])),
        td(input('', ["type","submit"], ["value","Chop!"],
            ["id","chop_submit"])),
        )),

    tr(concat(
        td('Create radio buttons:'),
        td(input('', ["type","submit"], ["value","Create!"],
            ["id","radio_make"])),
        td(),
        td(),
        )),

    tr(concat(
        td('Filter on:'),
        td(div(column_radio , ["id","xfilter"])),
        td(input('', ['type', 'text'], ['id', 'filter_val'])),
        td(input('', ["type","submit"], ["value","Filter!"],
            ["id","filter_submit"])),
        )),

    tr(concat(
        td('Go back'),
        td(input('', ["type","submit"], ["value","Previous Result"],
            ["id","prev_result"])),
        td(input('', ["type","submit"], ["value","Back to Data Set Selection"],
            ["id","to_control1"])),

        )),

        )) # table
        ) # sort_controls


inputs = div(concat(
    h1('Data Viewer'),
    form( table1, ["id","da_form"], ["method","post"] ),
    div( sort_controls,  ["id","div_sort"], ["class","hidden"] ),
    ), ['class', 'output'])

graphic = svg('', ['class', 'output'])

body = body(concat(
    div(concat(
        inputs,
        graphic,
    ), ['class', 'foo']),

    hr(),
    hr(),

    div(concat(
        pre( 'output area', ['class', 'output']),
        pre('secondary output area', ['class', 'output']),

    ), ['class', 'output'])

))

header =  "Content-type: text/html\n\n"
html_doc = header + html(head+body)
with open('data_viewer.html', 'w') as fh: fh.write(html_doc)
#print html_doc



