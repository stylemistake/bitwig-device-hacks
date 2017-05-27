from lib import atoms
from lib import util
from lib import fs

device_tooltip = '''
MUL - A × B
ADD - A + B
SUB - A - B
MIN - min(A, B)
MAX - max(A, B)
QUA - Quantize A, with step size B
DIV - A / B
ABS - abs(A)
SIG - sig(A)
SQR - A^2
POW - A^B
SQRT - sqrt(A)
EXP - e^A
LOG - log{b}(A)
LOG2 - log2(A)
LOG10 - log10(A)
LN - ln(A)
SIN - sin(2π × A) × B
COS - cos(2π × A) × B
TAN - cos(2π × A) × B
DELTA - ΔA × B
PS90 - 90° phase shift
'''.strip()

modes = [
    'MUL', 'ADD', 'SUB', 'MIN',
    'MAX', 'QUA', 'DIV', 'ABS',
    'SIG', 'SQR', 'POW', 'SQRT',
    'EXP', 'LOG', 'LOG2', 'LOG10',
    'LN', 'SIN', 'COS', 'TAN',
    'DELTA', 'PS90',
]

value_a = atoms.DecimalValue('A', min = -100, max = 100, step = 0.01)
value_b = atoms.DecimalValue('B', min = -100, max = 100, step = 0.01)
value_mode = atoms.IndexedValue('Mode', items = modes)

nitro_source = fs.read('mathx.nitro', __file__)
nitro = (atoms.Nitro()
    .add_inport(value_a)
    .add_inport(value_b)
    .add_inport(value_mode)
    .set_source(nitro_source))

mod_source = atoms.ModulationSource('MATH').add_inport(nitro)
poly_observer = atoms.PolyphonicObserver().add_inport(nitro)

grid_panel = (atoms.GridPanel()
    .add_item(atoms.MappingSourcePanelItem(model = mod_source)
        .set_position(0, 13))
    .add_item(atoms.PopupChooserPanelItem(model = value_mode)
        .set_tooltip(device_tooltip)
        .set_size(11, 4)
        .set_position(3, 0))
    .add_item(atoms.NumberFieldPanelItem(model = value_a, style = 2)
        .set_tooltip('Signal A')
        .set_position(2, 4)
        .with_value_bar())
    .add_item(atoms.NumberFieldPanelItem(model = value_b, style = 2)
        .set_tooltip('Signal B')
        .set_position(2, 9)
        .with_value_bar()))

modulator = (atoms.Modulator('Test')
    .set_description('Test device')
    .add_component(value_a)
    .add_component(value_b)
    .add_component(nitro)
    .add_component(mod_source)
    .add_component(poly_observer)
    .add_component(value_mode)
    .add_panel(atoms.Panel(grid_panel)))

device = modulator.serialize()
print(device)
