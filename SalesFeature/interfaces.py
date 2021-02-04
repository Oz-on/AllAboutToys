# Author: Oskar Domingos
# This file contains interfaces for different classes


class TabControllerInterface:
    def __create_view(self):
        raise NotImplementedError('__create_view method must be implemented')

    def __handle_back(self):
        raise NotImplementedError('__handle_back method must be implemented')

    def __open_subtab(self, subtab_to_open):
        raise NotImplementedError('__open_subtab method must be implemented')

    @property
    def view(self):
        raise NotImplementedError('view property method must be implemented')


class SubTabControllerInterface:
    def __create_view(self):
        raise NotImplementedError('__create_view method must be implemented')

    @property
    def view(self):
        raise NotImplementedError('view property method must be implemented')


class PreviewInterface:
    def remove(self):
        raise NotImplementedError('remove method must be implemented')

    def show(self):
        raise NotImplementedError('show method must be implemented')

    def __generate_view(self):
        raise NotImplementedError('__generate_view method must be implemented')
