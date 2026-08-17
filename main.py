from assistant import (
    speak,
    start_listening,
    get_command,
    stop_speaking
)

from core.registry import registry
from core.router import CommandRouter

from tools.register_tools import (
    register_all_tools
)


# ==========================================
# SAHVIA STARTUP
# ==========================================

def main():

    print()
    print("==========================================")
    print("              SAHVIA AI")
    print("==========================================")
    print("Voice-controlled computer agent")
    print("==========================================")
    print()


    # ==========================================
    # REGISTER TOOLS
    # ==========================================

    print(
        "🔧 Registering SAHVIA tools..."
    )

    register_all_tools()


    print(
        f"✅ {len(registry.list_tools())} tools registered."
    )


    # ==========================================
    # CREATE ROUTER
    # ==========================================

    router = CommandRouter(
        registry
    )


    # ==========================================
    # START SAHVIA
    # ==========================================

    speak(
        "Hello Saksham. "
        "I am Sahvia. "
        "I am ready."
    )


    # ==========================================
    # START MICROPHONE
    # ==========================================

    stop_background_listener = (
        start_listening()
    )


    try:

        while True:

            command = get_command()


            if not command:

                continue


            print()
            print(
                f"🎙️ Command received: {command}"
            )


            # ==================================
            # STOP COMMAND
            # ==================================

            if command == "__STOP__":

                print(
                    "🛑 Voice stopped."
                )

                stop_speaking()

                continue


            # ==================================
            # EXIT
            # ==================================

            if command in [

                "exit sahvia",
                "quit sahvia",
                "goodbye sahvia",
                "shutdown sahvia",
                "terminate sahvia"

            ]:

                speak(
                    "Goodbye Saksham."
                )

                break


            # ==================================
            # ROUTE
            # ==================================

            result = router.route(
                command
            )


            # ==================================
            # RESULT
            # ==================================

            if result.success:

                print(
                    f"✅ {result.message}"
                )

                if result.message:

                    speak(
                        result.message
                    )

            else:

                print(
                    f"❌ {result.error}"
                )

                speak(
                    "I couldn't complete that request."
                )


    except KeyboardInterrupt:

        print(
            "\n🛑 SAHVIA interrupted."
        )


    finally:

        stop_speaking()


        try:

            stop_background_listener(
                wait_for_stop=False
            )

        except Exception:

            pass


        print()
        print(
            "=========================================="
        )

        print(
            "SAHVIA stopped."
        )

        print(
            "=========================================="
        )


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":

    main()