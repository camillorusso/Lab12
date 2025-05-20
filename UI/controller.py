import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []
        self._currentCountry = None
        self._currentYear = None
        self._lista2 = []
        self._lista3 = []

    def fillDD_nations(self):
        self._listCountry = self._model.getAllNations()
        for element in self._listCountry:
            self._view.ddcountry.options.append(ft.dropdown.Option(text=element,
                                                                  data=element,
                                                                  on_click=self.read_DD_nations))

    def read_DD_nations(self, e):
        print("read_DD_nations called ")
        if e.control.data is None:
            self._currentCountry = None
        else:
            self._currentCountry = e.control.data
        print(self._currentCountry)

    def fillDD_years(self):
        self._listYear = ['2015', '2016', '2017', '2018']
        for element in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(text=element,
                                                                  data=element,
                                                                  on_click=self.read_DD_years))

    def read_DD_years(self, e):
        print("read_DD_years called ")
        if e.control.data is None:
            self._currentYear = None
        else:
            self._currentYear = e.control.data
        print(self._currentYear)

    def handle_graph(self, e):
        y = self._view.ddyear.value
        c = self._view.ddcountry.value
        if y is None:
            self._view.create_alert("Inserire un anno valido!")
            return
        else:
            year = int(y)
        if c is None:
            self._view.create_alert("Inserire una nazione valida!")
            return
        else:
            country = str(c)
        self._model.buildGraph(year, country)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Il grafo è stato correttamente creato."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {self._model.getNumNodes()} nodi."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {self._model.getNumEdges()} archi."))
        self._view.update_page()

    def handle_volume(self, e):
        if len(self._model._grafo.nodes) == 0:
            self._view.create_alert("Creare prima il grafo!")
            return
        self._view.txtOut2.controls.clear()
        lista1 = []
        for element in self._model._grafo.nodes:
            lista1.append((element.Retailer_name, self._model.getVolume(element)))
        self._lista2 = sorted(lista1, key=lambda p: p[1], reverse=True)
        for element in self._lista2:
            self._view.txtOut2.controls.append(ft.Text(f"{element[0]} --> {element[1]}"))
        self._view.update_page()

    def handle_path(self, e):
        if len(self._lista2) == 0:
            self._view.create_alert("Calcolare prima i volumi!")
            return
        n = self._view.txtN.value
        if n is None or int(n)<2:
            self._view.create_alert("Inserire un numero intero che sia maggiore o uguale a 2!")
            return
        else:
            num = int(n)
        for element in self._lista2:
            if element[1] != 0:
                self._lista3.append(self._model._idMapNome[element[0]])
        self._model.computePath(num, self._lista3)
        self._view.txtOut3.controls.append(
            ft.Text(f"Peso cammino massimo: {self._model.solBest}"))
        for element in self._model.path_edge:
            self._view.txtOut3.controls.append(ft.Text(
                f"{element[0].Retailer_name} --> {element[1].Retailer_name}: {str(element[2])}"))
        self._view.update_page()
