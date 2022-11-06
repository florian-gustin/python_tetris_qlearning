class TetriMino:
    ########################################### I
    mino_map = [
        [
                {
                    'GRID': [
                        [0, 0, 0, 0],
                        [1, 1, 1, 1],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]
                    ],
                    'BOUNDARIES': [1, 1, 1, 1],
                    'VOLUME': [1, 1, 1, 1],
                    'START_X': 0
                },
                {
                    'GRID': [
                        [0, 0, 1, 0],
                        [0, 0, 1, 0],
                        [0, 0, 1, 0],
                        [0, 0, 1, 0]
                    ],
                    'BOUNDARIES': [4],
                    'VOLUME': [4],
                    'START_X': 2
                },
                {
                    'GRID': [
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [1, 1, 1, 1],
                        [0, 0, 0, 0]
                    ],
                    'BOUNDARIES': [1, 1, 1, 1],
                    'VOLUME': [1, 1, 1, 1],
                    'START_X': 0
                }
,
                {
                    'GRID': [
                        [0, 1, 0, 0],
                        [0, 1, 0, 0],
                        [0, 1, 0, 0],
                        [0, 1, 0, 0]
                    ],
                    'BOUNDARIES': [4],
                    'VOLUME': [4],
                    'START_X': 1
                }

        ],
        ########################################### J
        [
                {
                    'GRID': [
                        [2, 0, 0, 0],
                        [2, 2, 2, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]
                    ],
                    'BOUNDARIES': [2, 1, 1],
                    'VOLUME': [2, 1, 1],
                    'START_X': 0
                }
,
                {
                    'GRID': [
                        [0, 2, 2, 0],
                        [0, 2, 0, 0],
                        [0, 2, 0, 0],
                        [0, 0, 0, 0]
                    ],
                    'BOUNDARIES': [3, 3],
                    'VOLUME': [3, 1],
                    'START_X': 1
                }
,
                {
                    'GRID': [
                        [0, 0, 0, 0],
                        [2, 2, 2, 0],
                        [0, 0, 2, 0],
                        [0, 0, 0, 0]
                    ],
                    'BOUNDARIES': [2, 2, 2],
                    'VOLUME': [1, 1, 2],
                    'START_X': 0
                }
,
                {
                    'GRID': [
                        [0, 2, 0, 0],
                        [0, 2, 0, 0],
                        [2, 2, 0, 0],
                        [0, 0, 0, 0]
                    ],
                    'BOUNDARIES': [1, 3],
                    'VOLUME': [1, 3],
                    'START_X': 0
                }

        ],
        ########################################### L
        [
                {
                    'GRID': [
                        [0, 0, 3, 0],
                        [3, 3, 3, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]
                    ],
                    'BOUNDARIES': [1, 1, 2],
                    'VOLUME': [1, 1, 2],
                    'START_X': 0
                }
,
                {
                    'GRID': [
                        [0, 3, 0, 0],
                        [0, 3, 0, 0],
                        [0, 3, 3, 0],
                        [0, 0, 0, 0]
                    ],
                    'BOUNDARIES': [3, 1],
                    'VOLUME': [3, 1],
                    'START_X': 1
                }
,
                {
                    'GRID': [
                        [0, 0, 0, 0],
                        [3, 3, 3, 0],
                        [3, 0, 0, 0],
                        [0, 0, 0, 0]
                    ],
                    'BOUNDARIES': [2, 2, 2],
                    'VOLUME': [2, 1, 1],
                    'START_X': 0
                }
,
                {
                    'GRID': [
                        [3, 3, 0, 0],
                        [0, 3, 0, 0],
                        [0, 3, 0, 0],
                        [0, 0, 0, 0]
                    ],
                    'BOUNDARIES': [3, 3],
                    'VOLUME': [1, 3],
                    'START_X': 0
                },
        ],
        ########################################### O
        [
                {
                    'GRID': [
                        [0, 4, 4, 0],
                        [0, 4, 4, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]
                    ],
                    'BOUNDARIES': [2, 2],
                    'VOLUME': [2, 2],
                    'START_X': 1
                },
                {
                    'GRID': [
                        [0, 4, 4, 0],
                        [0, 4, 4, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]
                    ],
                    'BOUNDARIES': [2, 2],
                    'VOLUME': [2, 2],
                    'START_X': 1
                },
                {
                    'GRID': [
                        [0, 4, 4, 0],
                        [0, 4, 4, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]
                    ],
                    'BOUNDARIES': [2, 2],
                    'VOLUME': [2, 2],
                    'START_X': 1
                },
                {
                    'GRID': [
                        [0, 4, 4, 0],
                        [0, 4, 4, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]
                    ],
                    'BOUNDARIES': [2, 2],
                    'VOLUME': [2, 2],
                    'START_X': 1
                }
        ],
        ########################################### S
        [
                {
                    'GRID': [
                        [0, 5, 5, 0],
                        [5, 5, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]
                    ],
                    'BOUNDARIES': [1, 2, 2],
                    'VOLUME': [1, 2, 1],
                    'START_X': 0
                },
                {
                    'GRID': [
                        [0, 5, 0, 0],
                        [0, 5, 5, 0],
                        [0, 0, 5, 0],
                        [0, 0, 0, 0]
                    ],
                    'BOUNDARIES': [3, 2],
                    'VOLUME': [2, 2],
                    'START_X': 1
                },
                {
                    'GRID': [
                        [0, 0, 0, 0],
                        [0, 5, 5, 0],
                        [5, 5, 0, 0],
                        [0, 0, 0, 0]
                    ],
                    'BOUNDARIES': [1, 2, 2],
                    'VOLUME': [1, 2, 1],
                    'START_X': 0
                },
                {
                    'GRID': [
                        [5, 0, 0, 0],
                        [5, 5, 0, 0],
                        [0, 5, 0, 0],
                        [0, 0, 0, 0]
                    ],
                    'BOUNDARIES': [3, 2],
                    'VOLUME': [2, 2],
                    'START_X': 0
                }
        ],
        ########################################### T
        [
                {
                    'GRID': [
                        [0, 6, 0, 0],
                        [6, 6, 6, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]
                    ],
                    'BOUNDARIES': [1, 2, 1],
                    'VOLUME': [1, 2, 1],
                    'START_X': 0
                },
                {
                    'GRID': [
                        [0, 6, 0, 0],
                        [0, 6, 6, 0],
                        [0, 6, 0, 0],
                        [0, 0, 0, 0]
                    ],
                    'BOUNDARIES': [3, 2],
                    'VOLUME': [3, 1],
                    'START_X': 1
                },
                {
                    'GRID': [
                        [0, 0, 0, 0],
                        [6, 6, 6, 0],
                        [0, 6, 0, 0],
                        [0, 0, 0, 0]
                    ],
                    'BOUNDARIES': [2, 2, 2],
                    'VOLUME': [1, 2, 1],
                    'START_X': 0
                },
                {
                    'GRID': [
                        [0, 6, 0, 0],
                        [6, 6, 0, 0],
                        [0, 6, 0, 0],
                        [0, 0, 0, 0]
                    ],
                    'BOUNDARIES': [2, 3],
                    'VOLUME': [1, 3],
                    'START_X': 0
                }
        ],
        ########################################### Z
        [
                {
                    'GRID': [
                        [7, 7, 0, 0],
                        [0, 7, 7, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]
                    ],
                    'BOUNDARIES': [2, 2, 1],
                    'VOLUME': [1, 2, 1],
                    'START_X': 0
                },
                {
                    'GRID': [
                        [0, 0, 7, 0],
                        [0, 7, 7, 0],
                        [0, 7, 0, 0],
                        [0, 0, 0, 0]
                    ],
                    'BOUNDARIES': [2, 3],
                    'VOLUME': [2, 2],
                    'START_X': 1
                },
                {
                    'GRID': [
                        [0, 0, 0, 0],
                        [7, 7, 0, 0],
                        [0, 7, 7, 0],
                        [0, 0, 0, 0]
                    ],
                    'BOUNDARIES': [2, 2, 1],
                    'VOLUME': [1, 2, 1],
                    'START_X': 0
                },
                {
                    'GRID': [
                        [0, 7, 0, 0],
                        [7, 7, 0, 0],
                        [7, 0, 0, 0],
                        [0, 0, 0, 0]
                    ],
                    'BOUNDARIES': [2, 3],
                    'VOLUME': [2, 2],
                    'START_X': 0
                }
        ]
    ]
