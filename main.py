from tests.conectividad_aerea import conectividad_aerea_mendoza
from tests.conectividad_terrestre import conectividad_terrestre_mendoza_regulares, conectividad_terrestre_mendoza_turisticos, conectividad_terrestre_pais, join_conectividad_terrestre
from tests.perfil_receptivo_internacional import perfil_receptivo_internacional, join_perfil_receptivo
from tests.turismo_internacional_receptivo import turismo_receptivo_internacional
import asyncio

async def main():
    # await conectividad_aerea_mendoza()
    await conectividad_terrestre_mendoza_regulares()
    # await conectividad_terrestre_mendoza_turisticos()
    # await join_conectividad_terrestre()
    # await conectividad_terrestre_pais()
    # await perfil_receptivo_internacional()
    # await turismo_receptivo_internacional()
    # await join_perfil_receptivo()

if __name__ == "__main__":
    asyncio.run(main())