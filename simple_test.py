# -*- coding: utf-8 -*-
"""
Egyszerű teszt - Stratos Digital Echo
"""

import asyncio


async def main():
    print("\n" + "=" * 60)
    print("STRATOS DIGITAL ECHO - EGYSZERŰ TESZT")
    print("=" * 60 + "\n")

    try:
        # Import
        print("[1/5] Importálás...")
        from stratos_digital_echo import StratosDigitalEchoAgent
        print("      OK - Import sikeres!\n")

        # Ágens létrehozása
        print("[2/5] Ágens létrehozása...")
        agent = StratosDigitalEchoAgent(name="simple_test")
        print("      OK - Ágens létrehozva!\n")

        # Inicializálás
        print("[3/5] Inicializálás...")
        await agent.initialize()
        print("      OK - Inicializálva!\n")

        # Template Manager ellenőrzése
        print("[4/5] Template Manager ellenőrzése...")
        if agent.template_manager:
            # Template statisztikák manuálisan
            print("      OK - Template Manager elérhető!\n")
        else:
            print("      HIBA - Nincs Template Manager!\n")

        # Kód generálás próba
        print("[5/5] Kód generálás...")
        print("-" * 60)

        result = await agent.generate_and_refine(
            prompt="Írj egy Python függvényt amely összeadja két számot",
            context={"language": "python"},
            iterations=1
        )

        print("\nGENERÁLT KÓD:")
        print("-" * 60)
        if result and result.code:
            print(result.code)
            print("-" * 60)
            print(f"Minőség: {result.score:.2f}")

            if result.score > 0.5:
                print("\n✓ SIKERES! A kód generálás működik!")
                return True
            else:
                print("\n? RÉSZLEGES - Alacsony minőség")
                return False
        else:
            print("(Üres eredmény)")
            print("-" * 60)
            print("\n× NEM SIKERÜLT - Nincs generált kód")
            return False

    except Exception as e:
        print(f"\n× HIBA: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n")
    success = asyncio.run(main())

    print("\n" + "=" * 60)
    if success:
        print("EREDMÉNY: SIKERES")
    else:
        print("EREDMÉNY: PROBLÉMÁK VANNAK")
    print("=" * 60 + "\n")
