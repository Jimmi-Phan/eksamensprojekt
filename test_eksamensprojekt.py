import pytest
import eksamensprojekt
from eksamensprojekt import fit_check, circles, wall_list

# Indstil globale parametre
eksamensprojekt.joints = 7
eksamensprojekt.hole_size = 50
eksamensprojekt.fit_check_size = 10

def test_fit_check_success():
    circles[:] = [
        (100, 100, 20),
        (200, 100, 20),
        (300, 100, 20),
        (400, 100, 20),
        (500, 100, 20),
        (600, 100, 20),
        (700, 100, 20),
    ]
    wall_list[:] = [[
        (100, 100),
        (200, 100),
        (300, 100),
        (400, 100),
        (500, 100),
        (600, 100),
        (700, 100),
    ]]

    assert fit_check(0) == True

def test_fit_check_fail_due_to_large_distance():
    circles[:] = [
        (100, 100, 20),
        (200, 100, 20),
        (300, 100, 20),
        (400, 100, 20),
        (500, 100, 20),
        (600, 100, 20),
        (800, 100, 20),  # Denne cirkel er for langt væk
    ]
    wall_list[:] = [[
        (100, 100),
        (200, 100),
        (300, 100),
        (400, 100),
        (500, 100),
        (600, 100),
        (700, 100),
    ]]

    assert fit_check(0) == False
