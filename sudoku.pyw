from view import View
from controller import Controller

controller = Controller()

view = View(controller.trace, controller.new_game)

nums = view.setup_view()

controller.start_controller(nums)

view.start_game()
