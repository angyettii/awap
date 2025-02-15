from src.player import Player
from src.map import Map
from src.robot_controller import RobotController
from src.game_constants import Team, Tile, GameConstants, Direction, BuildingType, UnitType

from src.units import Unit
from src.buildings import Building

class BotPlayer(Player):
    def __init__(self, map: Map):
        self.map = map
        self.swordsCount = 0
    
    def play_turn(self, rc: RobotController):
        
        team = rc.get_ally_team()
        ally_castle_id = -1

        ally_buildings = rc.get_buildings(team)
        for building in ally_buildings:
            if building.type == BuildingType.MAIN_CASTLE:
                ally_castle_id = rc.get_id_from_building(building)[1]
                break


        enemy = rc.get_enemy_team()
        enemy_castle_id = -1

        my_units = rc.get_unit_ids(team)
        enemy = rc.get_enemy_team()
        enemy_castle_id = -1


        if rc.can_spawn_unit(UnitType.SWORDSMAN, ally_castle_id) and self.swordsCount == 0:
            rc.spawn_unit(UnitType.SWORDSMAN, ally_castle_id)
            self.swordsCount += 1



        # like attack bot, attack all buildings
        enemy_units = rc.get_units(enemy)
        for e_unit in enemy_units:
            if e_unit.type == UnitType.KNIGHT:
                enemy_id = rc.get_id_from_unit(e_unit)[1]
                enemy_knight = rc.get_unit_from_id(enemy_id)
                if enemy_knight is None: 
                    continue
                # loop through all the units
                for unit_id in my_units:

                    # if castle still stands and can attack castle, attack castle
                    if rc.can_unit_attack_unit(unit_id, enemy_id):
                        rc.unit_attack_unit(unit_id, enemy_id)

                    # if can move towards castle, move towards castle
                    unit = rc.get_unit_from_id(unit_id)
                    if unit is None:
                        return
                    
                    possible_move_dirs = rc.unit_possible_move_directions(unit_id)
                    possible_move_dirs.sort(key= lambda dir: rc.get_chebyshev_distance(*rc.new_location(unit.x, unit.y, dir), enemy_knight.x, enemy_knight.y))

                    best_dir = possible_move_dirs[0] if len(possible_move_dirs) > 0 else Direction.STAY #least chebyshev dist direction

                    if rc.can_move_unit_in_direction(unit_id, best_dir):
                        rc.move_unit_in_direction(unit_id, best_dir)
        
        
        enemy_unit_id = -1
    
        # similar, attack all units
        enemy_units = rc.get_units(enemy)
        rc.unit_attack_unit(unit_id, enemy_unit_id)
        
        for e_unit in enemy_units:
            enemy_unit_id = rc.get_id_from_unit(e_unit)[0]
            enemy_unit = rc.get_unit_from_id(enemy_unit_id)
            
            if enemy_unit is None: 
                continue
            # loop through all the units
            for unit_id in my_units:

                # if castle still stands and can attack castle, attack castle
                if rc.can_unit_attack_unit(unit_id, enemy_unit):
                    rc.unit_attack_unit(unit_id, enemy_unit_id)

                # if can move towards castle, move towards castle
                unit = rc.get_unit_from_id(unit_id)
                if unit is None:
                    return
                
                possible_move_dirs = rc.unit_possible_move_directions(unit_id)
                possible_move_dirs.sort(key= lambda dir: rc.get_chebyshev_distance(*rc.new_location(unit.x, unit.y, dir), enemy_unit.x, enemy_unit.y))

                best_dir = possible_move_dirs[0] if len(possible_move_dirs) >= 0 else Direction.STAY #least chebyshev dist direction

                if rc.can_move_unit_in_direction(unit_id, best_dir):
                    rc.move_unit_in_direction(unit_id, best_dir)

        return

        # stage 1 : Defense/build phase


        # stage 2 : Attack phase 
        # only start attack phase if we have __ gold in the bank
        # and 

        
        
        