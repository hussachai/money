import random

# obtained from http://www.rapidtables.com/web/color/RGB_Color.htm
COLORS = ['#800000', '#8B0000', '#A52A2A', '#B22222', '#DC143C', '#FF0000', '#FF6347', '#FF7F50', '#CD5C5C',
          '#F08080', '#E9967A', '#FA8072', '#FFA07A', '#FF4500', '#FF8C00', '#FFA500', '#FFD700', '#B8860B',
          '#DAA520', '#EEE8AA', '#BDB76B', '#F0E68C', '#808000', '#FFFF00', '#9ACD32', '#556B2F', '#6B8E23',
          '#7CFC00', '#7FFF00', '#ADFF2F', '#006400', '#008000', '#228B22', '#00FF00', '#32CD32', '#90EE90',
          '#98FB98', '#8FBC8F', '#00FA9A', '#00FF7F', '#2E8B57', '#66CDAA', '#3CB371', '#20B2AA', '#2F4F4F',
          '#008080', '#008B8B', '#00FFFF', '#00FFFF', '#E0FFFF', '#00CED1', '#40E0D0', '#48D1CC', '#AFEEEE',
          '#7FFFD4', '#B0E0E6', '#5F9EA0', '#4682B4', '#6495ED', '#00BFFF', '#1E90FF', '#ADD8E6', '#87CEEB',
          '#87CEFA', '#191970', '#000080', '#00008B', '#0000CD', '#0000FF', '#4169E1', '#8A2BE2', '#4B0082',
          '#483D8B', '#6A5ACD', '#7B68EE', '#9370DB', '#8B008B', '#9400D3', '#9932CC', '#BA55D3', '#800080',
          '#D8BFD8', '#DDA0DD', '#EE82EE', '#FF00FF', '#DA70D6', '#C71585', '#DB7093', '#FF1493', '#FF69B4',
          '#FFB6C1', '#FFC0CB', '#FAEBD7', '#F5F5DC', '#FFE4C4', '#FFEBCD', '#F5DEB3', '#FFF8DC', '#FFFACD',
          '#FAFAD2', '#FFFFE0', '#8B4513', '#A0522D', '#D2691E', '#CD853F', '#F4A460', '#DEB887', '#D2B48C',
          '#BC8F8F', '#FFE4B5', '#FFDEAD', '#FFDAB9', '#FFE4E1', '#FFF0F5', '#FAF0E6', '#FDF5E6', '#FFEFD5',
          '#FFF5EE', '#F5FFFA', '#708090', '#778899', '#B0C4DE', '#E6E6FA', '#FFFAF0', '#F0F8FF', '#F8F8FF',
          '#F0FFF0', '#FFFFF0', '#F0FFFF', '#FFFAFA', '#000000', '#696969']

def random_color():
    return random.choice(COLORS)

