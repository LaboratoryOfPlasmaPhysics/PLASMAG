from numpy import pi, column_stack
from src.model.input_parameters import InputParameters
from src.model.strategies import CalculationStrategy
from scipy.constants import k


class NSD_R_cr(CalculationStrategy):
    """Analytical model for counter-reaction resistance (:math:`R_{CR}`) Noise Spectral Density

    .. math::

        NSD_{R_{CR}}(f) = \sqrt{\\frac{|4 . k . T . R_{CR}| . \omega^2 . (\\frac{M . H_1}{R_{CR}})^2}{(1 - L . C . \omega^2)^2 + \omega^2 . (R . C + \\frac{M . H_1}{R_{CR}})^2}}

    With:
        - :math:`k` : the Boltzmann constant
        - :math:`T` : the temperature
        - :math:`R_{CR}` : resistance of the counter-reaction coil
        - :math:`\omega = 2 \pi f`
        - :math:`f` : frequency
        - :math:`M` : Mutual inductance (coupling factor between the main coil and the feedback coil)
        - :math:`H_1` : transfer function of the ASIC's stage 1
        - :math:`R` : resistance of the coil
        - :math:`L` : inductance of the coil
        - :math:`C` : capacitance of the coil

    """

    def calculate(self, dependencies: dict, parameters: InputParameters):
        temperature = parameters.data["temperature"]
        feedback_resistance = parameters.data["feedback_resistance"]
        mutual_inductance = parameters.data["mutual_inductance"]
        h1 = dependencies["TF_ASIC_Stage_1"]["data"][:, 1]
        h2 = dependencies["TF_ASIC_Stage_2"]["data"][:, 1]
        frequency_vector = dependencies["frequency_vector"]["data"]
        nsd_normalisation = dependencies["NSD_normalisation"]["data"][:, 1]

        omega2 = (2 * pi * frequency_vector) ** 2
        numerator = abs(4 * k * temperature * feedback_resistance) * omega2 \
                    * (mutual_inductance * h1 / feedback_resistance) ** 2
        numerator = numerator ** 0.5
        nsd_non_filtered = numerator / nsd_normalisation
        nsd_filtered = nsd_non_filtered * h2

        results = column_stack((frequency_vector, nsd_non_filtered, nsd_filtered))

        return {
            "data": results,
            "labels": ["Frequency", "NSD_R_cr", "NSD_R_cr_filtered"],
            "units": ["Hz", "V/sqrt(Hz)", "V/sqrt(Hz)"]
        }

    @staticmethod
    def get_dependencies():
        return ["temperature", "feedback_resistance", "frequency_vector", "mutual_inductance",
                "TF_ASIC_Stage_1", "TF_ASIC_Stage_2", "NSD_normalisation"]


class NSD_R_Coil(CalculationStrategy):
    """Analytical model for coil resistance (:math:`R_{Coil}`) Noise Spectral Density

    .. math::

        NSD_{R_{Coil}}(f) = \sqrt{\\frac{|4 . k . T . R|}{(1 - L . C . \omega^2)^2 + \omega^2 . (R . C + \\frac{M . H_1}{R_{CR}})^2}}

    With:
        - :math:`k` : the Boltzmann constant
        - :math:`T` : the temperature
        - :math:`R` : resistance of the coil
        - :math:`\omega = 2 \pi f`
        - :math:`f` : frequency
        - :math:`M` : Mutual inductance (coupling factor between the main coil and the feedback coil)
        - :math:`H_1` : transfer function of the ASIC's stage 1
        - :math:`L` : inductance of the coil
        - :math:`C` : capacitance of the coil

    """

    def calculate(self, dependencies: dict, parameters: InputParameters):
        temperature = parameters.data["temperature"]
        R = dependencies["resistance"]["data"]
        nsd_normalisation = dependencies["NSD_normalisation"]["data"][:, 1]
        frequency_vector = dependencies["frequency_vector"]["data"]
        h2 = dependencies["TF_ASIC_Stage_2"]["data"][:, 1]

        numerator = abs(4 * k * temperature * R)
        numerator = numerator ** 0.5

        nsd_non_filtered = numerator / nsd_normalisation
        nsd_filtered = nsd_non_filtered * h2

        results = column_stack((frequency_vector, nsd_non_filtered, nsd_filtered))

        return {
            "data": results,
            "labels": ["Frequency", "NSD_R_Coil", "NSD_R_Coil_filtered"],
            "units": ["Hz", "V/sqrt(Hz)", "V/sqrt(Hz)"]
        }

    @staticmethod
    def get_dependencies():
        return ["temperature", "resistance", "frequency_vector", "NSD_normalisation",
                "TF_ASIC_Stage_2"]


class NSD_Flicker(CalculationStrategy):
    """Analytical model for flicker noise (:math:`NSD_{Flicker}`) Noise Spectral Density

    .. math::

        NSD_{flicker}(f) = \\frac{Para_A . 10^{-9}}{Para_B . f^\\frac{\\alpha}{10}} + e_{en}

    with:
        - :math:`Para_A` : fitting parameter adjusting the amplitude of the noise curve
        - :math:`Para_B` : fitting parameter adjusting the noise's frequency dependency
        - :math:`f` : frequency
        - :math:`\\alpha` : exponent parameter fine-tuning the frequency scaling
        - :math:`e_{en}` : equivalent input noise voltage

    """

    def calculate(self, dependencies: dict, parameters: InputParameters):
        Para_A = parameters.data["Para_A"]
        Para_B = parameters.data["Para_B"]
        Alpha = parameters.data["Alpha"]
        e_en = parameters.data["e_en"]
        frequency_vector = dependencies["frequency_vector"]["data"]

        Alpha /= 10
        nsd_non_filtered = Para_A * 1e-9 / (Para_B * (frequency_vector ** Alpha)) + e_en

        results = column_stack((frequency_vector, nsd_non_filtered))

        return {
            "data": results,
            "labels": ["Frequency", "NSD_Flicker"],
            "units": ["Hz", "V/sqrt(Hz)"]
        }

    @staticmethod
    def get_dependencies():
        return ["frequency_vector", "Para_A", "Para_B", "Alpha", "e_en"]


class NSD_e_en(CalculationStrategy):
    """Analytical model for equivalent input noise voltage (:math:`e_en`) Noise Spectral Density

    .. math::

        NSD_{e_{en}}(f) = \sqrt{\\frac{H_1^2(f) . NSD_{flicker}^2(f) . (1 - L . C . \omega^2)^2 + (\omega . R . C)^2}{(1 - L . C . \omega^2)^2 + \omega^2 . (R . C + \\frac{M . H_1(f)}{R_{CR}})^2}}

    With:
        - :math:`H_1` : transfer function of the ASIC's stage 1
        - :math:`NSD_{flicker}` : Noise Spectral Density of flicker noise
        - :math:`L` : inductance of the coil
        - :math:`C` : capacitance of the coil
        - :math:`\omega = 2 \pi f`
        - :math:`f` : frequency
        - :math:`R` : resistance of the coil
        - :math:`M` : Mutual inductance (coupling factor between the main coil and the feedback coil)
        - :math:`R_{CR}` : resistance of the counter-reaction coil

    """

    def calculate(self, dependencies: dict, parameters: InputParameters):
        flicker = dependencies["PSD_Flicker"]["data"][:, 1]
        h1 = dependencies["TF_ASIC_Stage_1"]["data"][:, 1]
        h2 = dependencies["TF_ASIC_Stage_2"]["data"][:, 1]
        L = dependencies["inductance"]["data"]
        C = dependencies["capacitance"]["data"]
        frequency_vector = dependencies["frequency_vector"]["data"]
        R = dependencies["resistance"]["data"]
        nsd_normalisation = dependencies["NSD_normalisation"]["data"][:, 1]

        omega2 = (2 * pi * frequency_vector) ** 2
        numerator = flicker ** 2 * h1 ** 2 * ((1 - omega2 * L * C) ** 2 + omega2 * (R * C) ** 2)
        numerator = numerator ** 0.5
        nsd_non_filtered = numerator / nsd_normalisation
        nsd_filtered = nsd_non_filtered * h2

        results = column_stack((frequency_vector, nsd_non_filtered, nsd_filtered))

        return {
            "data": results,
            "labels": ["Frequency", "NSD_e_en", "NSD_e_en_filtered"],
            "units": ["Hz", "V/sqrt(Hz)", "V/sqrt(Hz)"]
        }

    @staticmethod
    def get_dependencies():
        return ["PSD_Flicker", "TF_ASIC_Stage_1", "TF_ASIC_Stage_2", "inductance", "capacitance",
                "frequency_vector", "resistance", "NSD_normalisation"]


class NSD_e_in(CalculationStrategy):
    """Analytical model for input noise current (:math:`e_in`) Noise Spectral Density

    .. math::

        NSD_{e_{in}}(f) = \sqrt{\\frac{Z^2(f) . (e_{in} . 10^{-3})^2 . H_1^2(f) . (1 - L . C . \omega^2)^2 + (\omega . R . C)^2}{(1 - L . C . \omega^2)^2 + \omega^2 . (R . C + \\frac{M . H_1(f)}{R_{CR}})^2}}

    With:
        - :math:`Z` : Impedance
        - :math:`e_{in}` : the input noise current level
        - :math:`H_1` : transfer function of the ASIC's stage 1
        - :math:`L` : inductance of the coil
        - :math:`C` : capacitance of the coil
        - :math:`\omega = 2 \pi f`
        - :math:`f` : frequency
        - :math:`R` : resistance of the coil
        - :math:`M` : Mutual inductance (coupling factor between the main coil and the feedback coil)
        - :math:`R_{CR}` : resistance of the counter-reaction coil

    """

    def calculate(self, dependencies: dict, parameters: InputParameters):
        e_in = parameters.data["e_in"]
        impedance = dependencies["impedance"]["data"][:, 1]
        frequency_vector = dependencies["frequency_vector"]["data"]
        h1 = dependencies["TF_ASIC_Stage_1"]["data"][:, 1]
        h2 = dependencies["TF_ASIC_Stage_2"]["data"][:, 1]
        C = dependencies["capacitance"]["data"]
        R = dependencies["resistance"]["data"]
        L = dependencies["inductance"]["data"]
        nsd_normalisation = dependencies["NSD_normalisation"]["data"][:, 1]

        omega2 = (2 * pi * frequency_vector) ** 2
        numerator = impedance ** 2 * (e_in * 1e-3) ** 2 * h1 ** 2 \
                    * ((1 - L * C * omega2) ** 2 + omega2 * (R * C) ** 2)
        numerator = numerator ** 0.5
        nsd_non_filtered = numerator / nsd_normalisation
        nsd_filtered = nsd_non_filtered * h2

        results = column_stack((frequency_vector, nsd_non_filtered, nsd_filtered))

        return {
            "data": results,
            "labels": ["Frequency", "NSD_e_in", "NSD_e_in_filtered"],
            "units": ["Hz", "V/sqrt(Hz)", "V/sqrt(Hz)"]
        }

    @staticmethod
    def get_dependencies():
        return ["impedance", "e_in", "frequency_vector", "TF_ASIC_Stage_1", "TF_ASIC_Stage_2",
                "inductance", "capacitance", "resistance", "NSD_normalisation"]


class NSD_Total(CalculationStrategy):
    """Analytical model for total Noise Spectral Density

    .. math::

        NSD_{total}(f) = \sqrt{NSD_{e_{in}}^2(f) + NSD_{e_{en}}^2(f) + NSD_{R_{Coil}}^2(f) + NSD_{R_{CR}}^2(f)}

    With:
        - :math:`NSD_{e_{in}}` : input noise current (:math:`e_in`) Noise Spectral Density
        - :math:`NSD_{e_{en}}` : equivalent input noise voltage (:math:`e_en`) Noise Spectral Density
        - :math:`NSD_{R_{Coil}}` : coil resistance (:math:`R_{Coil}`) Noise Spectral Density
        - :math:`NSD_{R_{CR}}` : counter-reaction resistance (:math:`R_{CR}`) Noise Spectral Density

    """
    def calculate(self, dependencies: dict, parameters: InputParameters):
        nsd_e_in = dependencies["PSD_e_in"]["data"][:, 1]
        nsd_e_in_filtered = dependencies["PSD_e_in"]["data"][:, 2]
        nsd_e_en = dependencies["PSD_e_en"]["data"][:, 1]
        nsd_e_en_filtered = dependencies["PSD_e_en"]["data"][:, 2]
        nsd_r_coil = dependencies["PSD_R_Coil"]["data"][:, 1]
        nsd_r_coil_filtered = dependencies["PSD_R_Coil"]["data"][:, 2]
        nsd_r_cr = dependencies["PSD_R_cr"]["data"][:, 1]
        nsd_r_cr_filtered = dependencies["PSD_R_cr"]["data"][:, 2]
        frequency_vector = dependencies["frequency_vector"]["data"]

        total_non_filtered = (nsd_e_in**2 + nsd_e_en**2 + nsd_r_coil**2 + nsd_r_cr**2)**0.5
        total_filtered = (nsd_e_in_filtered**2 + nsd_e_en_filtered**2 + nsd_r_coil_filtered**2 + nsd_r_cr_filtered**2)**0.5
        values = column_stack((frequency_vector, total_non_filtered, total_filtered))

        return {
            "data": values,
            "labels": ["Frequency", "NSD_Total", "NSD_filtered_Total"],
            "units": ["Hz", "V/sqrt(Hz)", "V/sqrt(Hz)"]
        }

    @staticmethod
    def get_dependencies():
        return ["PSD_e_in", "PSD_e_en", "PSD_R_Coil", "PSD_R_cr", "frequency_vector"]


class Display_all_NSD(CalculationStrategy):

    def calculate(self, dependencies: dict, parameters: InputParameters):
        psd_e_in = dependencies["PSD_e_in"]["data"][:, 1]
        psd_e_en = dependencies["PSD_e_en"]["data"][:, 1]
        psd_r_coil = dependencies["PSD_R_Coil"]["data"][:, 1]
        psd_r_cr = dependencies["PSD_R_cr"]["data"][:, 1]
        psd_tot = dependencies["PSD_Total"]["data"][:, 1]
        frequency_vector = dependencies["frequency_vector"]["data"]

        values = column_stack((frequency_vector, psd_r_cr, psd_r_coil, psd_e_en, psd_e_in,
                               psd_tot))
        return {
            "data": values,
            "labels": ["Frequency", "NSD_R_cr", "NSD_R_Coil", "NSD_e_en", "NSD_e_in",
                       "NSD_Total"],
            "units": ["Hz", "V/sqrt(Hz)", "V/sqrt(Hz)", "V/sqrt(Hz)", "V/sqrt(Hz)", "V/sqrt(Hz)"]
        }

    @staticmethod
    def get_dependencies():
        return ["PSD_e_in", "PSD_e_en", "PSD_R_Coil", "PSD_R_cr", "frequency_vector", "PSD_Total"]


class Display_all_PSD(CalculationStrategy):

    def calculate(self, dependencies: dict, parameters: InputParameters):
        psd_e_in = dependencies["PSD_e_in"]["data"][:, 1]
        psd_e_en = dependencies["PSD_e_en"]["data"][:, 1]
        psd_r_coil = dependencies["PSD_R_Coil"]["data"][:, 1]
        psd_r_cr = dependencies["PSD_R_cr"]["data"][:, 1]
        psd_tot = dependencies["PSD_Total"]["data"][:, 1]
        frequency_vector = dependencies["frequency_vector"]["data"]

        psd_r_cr = psd_r_cr ** 2
        psd_r_coil = psd_r_coil ** 2
        psd_e_en = psd_e_en ** 2
        psd_e_in = psd_e_in ** 2
        psd_tot = psd_tot ** 2

        values = column_stack((frequency_vector, psd_r_cr, psd_r_coil, psd_e_en, psd_e_in,
                               psd_tot))
        return {
            "data": values,
            "labels": ["Frequency", "PSD_R_cr", "PSD_R_Coil",
                       "PSD_e_en", "PSD_e_in", "PSD_Total"],
            "units": ["Hz", "V^2/Hz", "V^2/Hz", "V^2/Hz", "V^2/Hz", "V^2/Hz"]
        }

    @staticmethod
    def get_dependencies():
        return ["PSD_e_in", "PSD_e_en", "PSD_R_Coil", "PSD_R_cr", "frequency_vector", "PSD_Total"]


class Display_all_NSD_filtered(CalculationStrategy):

    def calculate(self, dependencies: dict, parameters: InputParameters):
        psd_e_in = dependencies["PSD_e_in"]["data"][:, 2]
        psd_e_en = dependencies["PSD_e_en"]["data"][:, 2]
        psd_r_coil = dependencies["PSD_R_Coil"]["data"][:, 2]
        psd_r_cr = dependencies["PSD_R_cr"]["data"][:, 2]
        psd_tot = dependencies["PSD_Total"]["data"][:, 2]
        frequency_vector = dependencies["frequency_vector"]["data"]

        values = column_stack((frequency_vector, psd_r_cr, psd_r_coil, psd_e_en, psd_e_in,
                               psd_tot))
        return {
            "data": values,
            "labels": ["Frequency", "NSD_R_cr_filtered", "NSD_R_Coil_filtered",
                       "NSD_e_en_filtered", "NSD_e_in_filtered",
                       "NSD_filtered_Total"],
            "units": ["Hz", "V/sqrt(Hz)", "V/sqrt(Hz)", "V/sqrt(Hz)", "V/sqrt(Hz)", "V/sqrt(Hz)"]
        }

    @staticmethod
    def get_dependencies():
        return ["PSD_e_in", "PSD_e_en", "PSD_R_Coil", "PSD_R_cr", "frequency_vector", "PSD_Total"]


class Display_all_PSD_filtered(CalculationStrategy):

    def calculate(self, dependencies: dict, parameters: InputParameters):
        psd_e_in = dependencies["PSD_e_in"]["data"][:, 2]
        psd_e_en = dependencies["PSD_e_en"]["data"][:, 2]
        psd_r_coil = dependencies["PSD_R_Coil"]["data"][:, 2]
        psd_r_cr = dependencies["PSD_R_cr"]["data"][:, 2]
        psd_tot = dependencies["PSD_Total"]["data"][:, 2]
        frequency_vector = dependencies["frequency_vector"]["data"]

        psd_r_cr = psd_r_cr ** 2
        psd_r_coil = psd_r_coil ** 2
        psd_e_en = psd_e_en ** 2
        psd_e_in = psd_e_in ** 2
        psd_tot = psd_tot ** 2

        values = column_stack((frequency_vector, psd_r_cr, psd_r_coil, psd_e_en, psd_e_in,
                               psd_tot))
        return {
            "data": values,
            "labels": ["Frequency", "PSD_R_cr_filtered", "PSD_R_Coil_filtered",
                       "PSD_e_en_filtered", "PSD_e_in_filtered", "PSD_filtered_Total"],
            "units": ["Hz", "V^2/Hz", "V^2/Hz", "V^2/Hz", "V^2/Hz", "V^2/Hz"]
        }

    @staticmethod
    def get_dependencies():
        return ["PSD_e_in", "PSD_e_en", "PSD_R_Coil", "PSD_R_cr", "frequency_vector", "PSD_Total"]


class NEMI(CalculationStrategy):

    def calculate(self, dependencies: dict, parameters: InputParameters):
        psd = dependencies["PSD_Total"]["data"][:, 1]
        psd_filtered = dependencies["PSD_Total"]["data"][:, 2]
        cltf = dependencies["CLTF"]["data"][:, 1]
        frequency_vector = dependencies["frequency_vector"]["data"]

        nemi_non_filtered = psd / cltf
        nemi_filtered = psd_filtered / cltf
        results = column_stack((frequency_vector, nemi_non_filtered, nemi_filtered))

        return {
            "data": results,
            "labels": ["Frequency", "NEMI", "NEMI_filtered"],
            "units": ["Hz", "T/sqrt(Hz)", "T/sqrt(Hz)"]
        }

    @staticmethod
    def get_dependencies():
        return ["PSD_Total", "CLTF", "frequency_vector"]


class NSD_normalisation(CalculationStrategy):
    """Convenience strategy to compute only once the Noise Spectral Density denominator"""

    def calculate(self, dependencies: dict, parameters: InputParameters):
        R = dependencies["resistance"]["data"]
        L = dependencies["inductance"]["data"]
        C = dependencies["capacitance"]["data"]
        mutual_L = parameters.data["mutual_inductance"]
        h1 = dependencies["TF_ASIC_Stage_1"]["data"][:, 1]
        R_feedback = parameters.data["feedback_resistance"]
        frequency_vector = dependencies["frequency_vector"]["data"]
        omega2 = (2 * pi * frequency_vector) ** 2
        denominator = ((1 - L * C * omega2) ** 2
                       + omega2 * (R * C + h1 * mutual_L / R_feedback) ** 2)
        denominator = denominator ** 0.5

        results = column_stack((frequency_vector, denominator))

        return {
            "data": results,
            "labels": ["Frequency", "NSD_normalisation"],
            "units": ["Hz", " "]
        }

    @staticmethod
    def get_dependencies():
        return ["inductance", "feedback_resistance", "frequency_vector", "mutual_inductance",
                "TF_ASIC_Stage_1", "capacitance", "resistance"]
