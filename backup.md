classDiagram
direction BT
class node11 {
    __grid
    __cat_box
    __game_pos_y
    __game_pos_x
    __grid
    __game_pos_x
    __game_pos_y
    __cat_box
   __init__(self) 
   __repr__(self) 
   increase_coordinates(self, x, y) 
   update_cordinates(self, new_x, new_y) 
   get_grid(self) 
   get_grid_size(self) 
   get_cat_box(self) 
   set_grid(self, new_grid) 
   set_cat_box(self, new_cat) 
   get_game_pos(self) 
   get_game_pos_x(self) 
   get_game_pos_y(self) 
   update(self) 
}
class node12 {
    sprites
    my_font
   __init__(self) 
   draw(self, surface, player=None, board=None, this_single_square=None, object=None, inventory=None, pos_x=None,
             pos_y=None, draw_scale=1) 
   draw_player(self, surface: pygame, player, board, draw_scale=1) 
   draw_object(self, surface: pygame, object, board, pos_x, pos_y, draw_scale=1) 
   draw_inventory(self, surface: pygame, inventory, ) 
   draw_single_square(self, surface: pygame, single_square, board, pos_x, pos_y, draw_scale = 1) 
   draw_board(self, surface: pygame, board) 
}
class node9 {
   __init__(self) 
}
class node0 {
    __start_of_active
    _type
    __is_active
    _skin
    _skin
    _type
    input
    output
    fuel
    __input_resources
    __output_resources
    __alowded_fuel
    __is_active
    __start_of_active
   __init__(self) 
   __repr__(self) 
   change_active(self) 
   change_skin(self) 
   update(self) 
}
class node6 {
    _skin
    is_player_available
   __init__(self) 
}
class node8 {
    date
    debug
    warnings
    errors
    info
   __init__(self) 
   add_str_to_file(self, str_to_write, file_name) 
   add_info(self, text) 
   add_warnings(self, text) 
   add_errors(self, text) 
   add_debug(self, text) 
}
class node7 {
    _skin
    _resource
    _amount
    _resource
    _amount
    _skin
   __init__(self, resource=None, amount=None, skin=None) 
   __repr__(self) 
   get_resource(self) 
   get_skin(self) 
}
class node13 {
    __skin
    __direction
    __name
    __inventory
    __y
    __x
    __settings
    __status
    statuses
   __init__(self, name="Mihaham", position_x=0, position_y=0, skin="sprites/bottom.png", settings=None) 
   __repr__(self) 
   move(self, event, board=None) 
   update_skin(self) 
   get_inventory(self) 
   get_status(self) 
   get_name(self) 
   rename(self, new_name) 
   get_skin(self) 
   get_direction(self) 
   get_position(self) 
   get_x(self) 
   get_y(self) 
   set_direction(self, new_direction) 
   update_position(self, position) 
   update(self, board) 
}
class node10 {
    _is_burnable
    _skin
    _skin
    _is_burnable
   __from_prototipe(self, prototipe) 
   __init__(self, prototipe=None) 
   get_skin(self) 
   get_is_burnable(self) 
   copy(self) 
}
class node2 {
    __id
    _miners
    _buildings
    _resources
    _skin
    is_player_available
    __id
   __take_prototipe__(self, prototipe) 
   __init__(self, skin=None, prototipe=None) 
   __repr__(self) 
   set_skin(self, skin=None, prototipe=None) 
   get_skin(self) 
   add_object(self, object) 
   get_buildings(self) 
   get_miners(self) 
   copy(self) 
   update(self) 
   add_miner(self, miner) 
   mine(self) 
   get_resources(self) 
}
class node5 {
    _is_burnable
    _skin
   __init__(self) 
}
class node15 {
   __init__(self) 
}
class node1 {
    _skin
    is_player_available
   __init__(self) 
}
class node14 {
    _is_burnable
    _skin
   __init__(self) 
}
class node3 {
    _selected_item
    _cursor
    _is_selected
    _size_x
    _scale
    _size_y
    _grid
   __init__(self, size_x=5, size_y=10) 
   __repr__(self) 
   get_selected_item(self) 
   get_cursor(self) 
   get_sizes(self) 
   add_item(self, item, pos=None) 
   move_right(self) 
   move_left(self) 
   move_up(self) 
   move_down(self) 
   select(self) 
   take_item(self) 
   get_grid(self) 
   is_selected(self) 
}
class node4 {
   __hash__(self) 
}

node7  -->  node9 
node2  -->  node6 
node10  -->  node5 
node7  -->  node15 
node2  -->  node1 
node10  -->  node14 
