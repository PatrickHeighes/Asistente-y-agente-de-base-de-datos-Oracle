from chat_with_AI.mode_AI import ModelAI

def iniciar_chat():
    print("==================================================")
    print("      🤖 CHAT INTELIGENTE CON ORACLE & IA         ")
    print("==================================================")
    print("Comandos disponibles:")
    print("  /mode ask   -> Modo pregunta general / código")
    print("  /mode agent -> Modo agente (Interactúa con Oracle con confirmación)")
    print("  /exit       -> Salir del chat")
    print("==================================================")

    ia = ModelAI()
    modo_actual = "agent"  
    print(f"\n[Modo actual: {modo_actual.upper()}]")

    while True:
        try:
            user_input = input(f"\n({modo_actual}) > ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "/exit":
                print("¡Hasta luego!")
                break
            elif user_input.lower() == "/mode ask":
                modo_actual = "ask"
                print("🔄 Cambiado a MODO ASK.")
                continue
            elif user_input.lower() == "/mode agent":
                modo_actual = "agent"
                print("🔄 Cambiado a MODO AGENT.")
                continue

            if modo_actual == "ask":
                print("\n🧠 Analizando pregunta...")
                respuesta = ia.modo_ask(user_input)
                print(f"\nRespuesta:\n{respuesta}")
            
            elif modo_actual == "agent":
                print("\n🔍 Analizando solicitud y preparando plan de acción...")
                analisis = ia.modo_agent_analisis(user_input)
                
                if "error" in analisis:
                    print(f"\n❌ {analisis['error']}")
                    continue
                
                # Mostrar estructura analítica al usuario
                print("\n--------------------------------------------------")
                print(f"📋 **Entendimiento:** {analisis.get('entendimiento')}")
                gravedad = str(analisis.get('gravedad', 'desconocida')).upper()
                print(f"⚠️ **Gravedad de la acción:** {gravedad}")
                print(f"🛠️ **SQL Proyectado:**\n{analisis.get('sql')}")
                print("--------------------------------------------------")
                
                # Pedir confirmación obligatoria Sí / No
                confirmacion = input("¿Deseas autorizar y ejecutar esta acción en la base de datos? (sí / no): ").strip().lower()
                
                if confirmacion in ["sí", "si", "s", "yes"]:
                    sql_a_ejecutar = analisis.get("sql")
                    if not sql_a_ejecutar:
                        print("❌ No hay una sentencia SQL válida para ejecutar.")
                        continue
                        
                    print("\n⚡ Ejecutando en Oracle DB...")
                    resultado = ia.ejecutar_consulta_sql(sql_a_ejecutar)
                    
                    if "error" in resultado:
                        print(f"\n❌ **Error exacto en Oracle:** {resultado['error']}")
                    else:
                        if resultado.get("tipo") == "select":
                            print(f"\n✅ **¡Consulta ejecutada con éxito!**")
                            print(f"📊 **Resultados obtenidos de la BD:**")
                            
                            # Imprimir columnas y filas ordenadas
                            cols = resultado.get("columns", [])
                            rows = resultado.get("rows", [])
                            print(" | ".join(cols))
                            print("-" * 50)
                            for row in rows:
                                print(" | ".join(str(val) for val in row))
                                
                            print(f"\n💡 **Explicación del Agente:** El análisis detallado muestra el cliente top de cada país según su LTV (Lifetime Value). Esto ayuda al negocio a identificar mercados clave y los compradores de mayor valor en la base de datos Chinook.")
                        else:
                            print(f"\n✅ **¡Acción ejecutada con éxito!**")
                            print(f"📊 **Resultado:** {resultado.get('message')}")
                else:
                    print("\n🚫 Operación cancelada por el usuario.")

        except KeyboardInterrupt:
            print("\n\nSaliendo del chat...")
            break
        except Exception as e:
            print(f"\n❌ Ocurrió un error inesperado: {e}")