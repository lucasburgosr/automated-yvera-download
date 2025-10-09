from tests.conectividad_aerea import conectividad_aerea_mendoza
from tests.conectividad_terrestre import conectividad_terrestre_mendoza, conectividad_terrestre_pais
from tests.perfil_receptivo_internacional import perfil_receptivo_internacional
from tests.turismo_internacional_receptivo import turismo_receptivo_internacional

async def main():
    await conectividad_aerea_mendoza()
    await conectividad_terrestre_mendoza()
    await conectividad_terrestre_pais()
    await perfil_receptivo_internacional()
    await turismo_receptivo_internacional()
