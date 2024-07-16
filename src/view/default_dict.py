input_parameters = {
    "CORE" : {
'mu_insulator': {
        'default': 1, 'min': 0, 'max': 10,
        'description': "Permeability of the insulator",
        'input_unit': '', 'target_unit': ''
    },
    'kapton_thick': {
        'default': 30, 'min': 10, 'max': 300,
        'description': "Thickness of the kapton in micrometers",
        'input_unit': 'micrometer', 'target_unit': 'meter'
    },
    'insulator_thick': {
        'default': 10, 'min': 1, 'max': 100,
        'description': "Thickness of the insulator in micrometers",
        'input_unit': 'micrometer', 'target_unit': 'meter'
    },
    'diam_out_mandrel': {
        'default': 3.2, 'min': 1, 'max': 10,
        'description': "Diameter of the outer mandrel in millimeters",
        'input_unit': 'millimeter', 'target_unit': 'meter'
    },
    'len_core': {
        'default': 20, 'min': 1, 'max': 200,
        'description': "Length of the core in centimeters",
        'input_unit': 'centimeter', 'target_unit': 'meter'
    },
    'diam_core': {
        'default': 3.2, 'min': 1, 'max': 100,
        'description': "Diameter of the core in millimeters",
        'input_unit': 'millimeter', 'target_unit': 'meter'
    },
    },

    "COIL" :
        {
'mu_r': {
        'default': 100000, 'min': 1, 'max': 1000000,
        'description': "Relative permeability",
        'input_unit': '', 'target_unit': ''
    },
            'len_coil': {
                'default': 155, 'min': 1, 'max': 200,
                'description': "Length of the coil in millimeters",
                'input_unit': 'millimeter', 'target_unit': 'meter'
            },
    'nb_spire': {
        'default': 12100, 'min': 1000, 'max': 20000,
        'description': "Number of spires",
        'input_unit': '', 'target_unit': ''
    },
    'ray_spire': {
        'default': 5, 'min': 1, 'max': 100,
        'description': "Radius of the spire in millimeters",
        'input_unit': 'millimeter', 'target_unit': 'meter'
    },
    'rho_wire': {
        'default': 1.6, 'min': 1, 'max': 10,
        'description': "Resistivity of the wire",
        'input_unit': '', 'target_unit': ''
    },
    'coeff_expansion': {
        'default': 1, 'min': 1, 'max': 10,
        'description': "Expansion coefficient",
        'input_unit': '', 'target_unit': ''
    },
    'diam_wire': {
        'default': 90, 'min': 10, 'max': 300,
        'description': "Diameter of the wire in micrometers",
        'input_unit': 'micrometer', 'target_unit': 'meter'
    },
    'capa_tuning': {
        'default': 1, 'min': 1, 'max': 1000,
        'description': "Tuning capacitance in picofarads",
        'input_unit': 'picofarad', 'target_unit': 'farad'
    },
    'capa_triwire': {
        'default': 150, 'min': 10, 'max': 1000,
        'description': "Triwire capacitance in picofarads",
        'input_unit': 'picofarad', 'target_unit': 'farad'
    },
        },




    'ASIC' : {
'stage_1_cutting_freq': {
        'default': 100, 'min': 1, 'max': 1000000,
        'description': "Cutting frequency of the first stage in Hertz",
        'input_unit': 'hertz', 'target_unit': 'hertz'
    },

    'stage_2_cutting_freq': {
        'default': 20000, 'min': 1, 'max': 1000000,
        'description': "Cutting frequency of the second stage in Hertz",
        'input_unit': 'hertz', 'target_unit': 'hertz'
    },

    'gain_1_linear': {
        'default': 1, 'min': 1, 'max': 1000,
        'description': "Gain of the first stage in linear",
        'input_unit': '', 'target_unit': ''
    },
    'gain_2_linear': {
        'default': 1, 'min': 1, 'max': 1000,
        'description': "Gain of the second stage in linear",
        'input_unit': '', 'target_unit': ''
    },

    },





    'misc': {
        'mutual_inductance': {
                'default': 1, 'min': 0, 'max': 1,
                'description': "Mutual inductance",
                'input_unit': '', 'target_unit': ''
            },
'feedback_resistance': {
        'default': 1000, 'min': 1, 'max': 100000,
        'description': "Feedback resistance in Ohms",
        'input_unit': 'ohm', 'target_unit': 'ohm'
    },
        'f_start': {
            'default': 0.1, 'min': 0.1, 'max': 1000,
            'description': "Start frequency in Hertz",
            'input_unit': 'hertz', 'target_unit': 'hertz'
        },
        'f_stop': {
            'default': 100000, 'min': 1000, 'max': 100000,
            'description': "Stop frequency in Hertz",
            'input_unit': 'hertz', 'target_unit': 'hertz'
        },
        'nb_points_per_decade': {
            'default': 100, 'min': 10, 'max': 1000,
            'description': "Number of points per decade",
            'input_unit': '', 'target_unit': ''
        },
    }

}
