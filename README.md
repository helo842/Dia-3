# Gilded Rose Kata

Kata clásica de **refactorización** (originariamente [Emily Bache](https://github.com/emilybache/GildedRose-Refactoring-Kata)). El objetivo no es añadir features a ciegas, sino **entender el código legado, cubrirlo con tests y dejarlo más claro** sin cambiar el comportamiento.

Este repositorio contiene una implementación en Python de `GildedRose.update_quality()` y una batería de tests con pytest.

## El problema

Gilded Rose es una posada que vende artículos de calidad variable. Cada artículo tiene:

| Campo | Significado |
| --- | --- |
| `name` | Nombre del artículo |
| `sell_in` | Días restantes para venderlo |
| `quality` | Valor del artículo |

Al final de cada día, el sistema actualiza `sell_in` y `quality` de todos los artículos.

## Reglas de negocio

Reglas generales:

- La calidad **nunca es negativa**.
- La calidad **nunca supera 50** (salvo Sulfuras, que es un artículo legendario).
- Cuando `sell_in` pasa a ser negativo, la calidad se degrada **el doble de rápido**.

Artículos especiales:

| Artículo | Comportamiento |
| --- | --- |
| Artículos normales | La calidad baja 1 cada día (2 si ya está caducado). |
| **Aged Brie** | La calidad **sube** 1 cada día (2 si está caducado). |
| **Sulfuras, Hand of Ragnaros** | No cambia ni `sell_in` ni `quality`. |
| **Backstage passes to a TAFKAL80ETC concert** | La calidad sube 1; **+2** con 10 días o menos; **+3** con 5 días o menos; **cae a 0** tras el concierto. |

## Estructura del proyecto

```
.
├── gilded_rose.py       # Lógica de actualización de inventario
├── test_gilded_rose.py  # Tests unitarios (pytest)
└── README.md
```

- `GildedRose`: recorre el inventario y aplica las reglas anteriores.
- `Item`: modelo simple (`name`, `sell_in`, `quality`). No se modifica su API.

## Requisitos

- Python 3.10 o superior (probado con Python 3.14)
- [pytest](https://pytest.org/)

## Cómo ejecutar los tests

```bash
pip install pytest
pytest -v
```

En Windows, si `python` no está en el PATH:

```bash
py -m pip install pytest
py -m pytest -v
```

Deberían pasar **44 tests** que cubren artículos normales, Aged Brie, Sulfuras, Backstage passes, inventario vacío o mixto, y el tope de calidad.

## Qué se ha trabajado aquí

1. Extraer la lógica de `update_quality` en métodos más pequeños y con nombres explícitos.
2. Fijar el comportamiento con tests unitarios (casos límite: calidad 0 y 50, umbrales de 11/10/6/5 días, caducidad).
3. Dejar una base segura para ampliar el sistema (por ejemplo, artículos *Conjured*) sin romper las reglas existentes.

## Licencia

Uso educativo. El enunciado original de la kata es de [Terry Hughes](https://github.com/NotMyself/GildedRose) y la versión de refactoring de Emily Bache.
