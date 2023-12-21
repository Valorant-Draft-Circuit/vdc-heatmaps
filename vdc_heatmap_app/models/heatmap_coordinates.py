from collections import Counter
from typing import Any, List, Dict
from pydantic import BaseModel
import numpy as np
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt


class Heatmap(BaseModel):
    """
    Represents the data for a heatmap.

    Attributes:
        coordinates (List[Dict[str, float]]): The list of coordinate dictionaries.
        played_map (str): The name of the played map.
        event (bool): Indicates if an event occurred.
        isAccurate (bool, optional): Indicates if a heatmap is wanted(True) or pixel accurate data is preferred(False). Defaults to False.
    """

    coordinates: List[Dict[str, float]]
    played_map: str
    event: str
    isAccurate: bool = False
    sigma: int = 16
    image_id: str = ""
    _formatted_data: Dict[str, Any] = {}

    def __format_for_heatmap(self):
        """
        Formats the data for a heatmap.

        ## Parameters:
            None

        ## Returns:
            formatted_data (dict): A dictionary containing the formatted data, including:
                - map_array: A 2D numpy array representing the heatmap.
                - xedges: The bin edges along the x-axis.
                - yedges: The bin edges along the y-axis.
                - freq: A list of the frequency of each coordinate in the heatmap.
                - coordinates: A list of the (x, y) coordinates used to generate the heatmap.
                - map_played: The map that was played during the match.
                - event: The event that is being plotted on the heatmap.

        ## Raises:
            Exception: If the coordinate list is not in the correct format.
        """
        try:
            self.coordinates = [(coord["x"], coord["y"]) for coord in self.coordinates]
            coordinates_counter = Counter(self.coordinates)
            x, y = zip(*coordinates_counter.keys())
            freq = list(coordinates_counter.values())

            map_value_array, xedges, yedges = np.histogram2d(
                x, y, bins=(np.arange(0, 1024), np.arange(0, 1024))
            )
            map_value_array = gaussian_filter(map_value_array, sigma=self.sigma)

            self._formatted_data = {
                "map_array": map_value_array,
                "xedges": xedges,
                "yedges": yedges,
                "freq": freq,
                "xy_coordinates": [x, y],
            }

        except TypeError as e:
            raise Exception("Coordinate list is not in the correct format") from e

    def __create_heatmap(self) -> None:
        """
        Creates a heatmap from a dictionary of formatted data.

        ## Parameters:
            formatted_data (dict): A dictionary containing the formatted data, including:
                - map_array: A 2D numpy array representing the heatmap.
                - xedges: The bin edges along the x-axis.
                - yedges: The bin edges along the y-axis.
                - freq: A list of the frequency of each coordinate in the heatmap.
                - coordinates: A list of the (x, y) coordinates used to generate the heatmap.
                - map_played: The map that was played during the match.
                - event: The event that is being plotted on the heatmap.
        """
        map_img: np.ndarray[Any, Any] = plt.imread(
            f"/vdc_app/vdc_heatmap_app/resources/maps/{self.played_map}.png"
        )
        if self.isAccurate:
            plt.imshow(map_img)
            plt.scatter(
                self._formatted_data["xy_coordinates"][0],
                self._formatted_data["xy_coordinates"][1],
                c=self._formatted_data["freq"],
                cmap="jet",
                s=10,
                marker="o",
            )
            plt.colorbar(label=f"{self.event} frequency")
            plt.axis("off")
            plt.savefig(
                f"/vdc_app/vdc_heatmap_app/resources/precisemaps/{self.played_map}-{self.event}-precise.png",
                bbox_inches="tight",
                pad_inches=0,
            )
            self.image_id = f"{self.played_map}-{self.event}-precise.png"
        if self.isAccurate == False:
            plt.imshow(
                map_img,
                extent=[
                    self._formatted_data["xedges"][0],
                    self._formatted_data["xedges"][-1],
                    self._formatted_data["yedges"][0],
                    self._formatted_data["yedges"][-1],
                ],
                origin="lower",
            )
            plt.imshow(self._formatted_data["map_array"].T, cmap="jet", alpha=0.3)
            plt.colorbar(label=f"{self.event} frequency")
            plt.axis("off")
            plt.savefig(
                f"/vdc_app/vdc_heatmap_app/resources/heatmaps/{self.played_map}-{self.event}-heatmap.png",
                bbox_inches="tight",
                pad_inches=0,
            )
            self.image_id = f"{self.played_map}-{self.event}-heatmap.png"
        plt.close()

    def generate_heatmap(self) -> None:
        """
        Generates a heatmap from the given data.

        ## Parameters:
            None

        ## Returns:
            None

        The heatmap is created and saved to the resources/heatmaps directory.
        """
        self.__format_for_heatmap()
        self.__create_heatmap()
