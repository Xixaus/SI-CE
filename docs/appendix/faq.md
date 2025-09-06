# Frequently Asked Questions

Common questions and solutions for SI-CE integration workflows.

## Overview

### What is SI-CE?

SI-CE is a comprehensive Python package that seamlessly integrates Sequential Injection (SI) with Capillary Electrophoresis (CE) through Agilent ChemStation. This powerful combination enables complete laboratory automation including:

- **Automated sample preparation** - Streamlined sample handling and preparation workflows
- **CE instrument control** - Direct communication with ChemStation for method execution
- **Batch analysis workflows** - Process multiple samples with minimal manual intervention  
- **Complete analytical automation** - End-to-end automation from sample prep to data analysis

### Hardware Compatibility

**Supported ChemStation Systems:**

- Tato verze byla vyvíjena a testována na Openlab ChemStation ver. C.01.07 SR2 [255] s CE 7100
- Funkčnost rozhraní byla testována i na jiných verzích Chemstationů a připojených přístrojů ovšem není zaručená funkčnost vytvořených funkcí
- Rozhraní nevunguje kvůli absenci command procesoru a nepodpoře maker na OpenLab CDS 2.x

**SIA Components:**

- VICI/Valco valve selectors and switching systems
- Compatible third-party devices with similar commands
- Additional components can be integrated and will be supported in future releases

### Programming Requirements

While basic Python knowledge is helpful, extensive programming experience is not required. The package is designed for accessibility:

- **High-level workflow methods** - Simple functions for complex operations
- **Pre-built analytical procedures** - Ready-to-use templates for common analyses
- **Copy-paste examples** - Working code snippets you can adapt immediately
- **Comprehensive documentation** - Detailed guides and tutorials

**AI-Assisted Development:** You can leverage generative AI tools (ChatGPT, Claude, etc.) by providing them with the repository link. These tools can help you program custom methods tailored to your specific needs. However, always thoroughly test any AI-generated code before implementation in production workflows.

## Communication and Control

### Monitoring ChemStation Communication

**Q: How can I monitor what commands are being sent to ChemStation?**

**A: Enable verbose logging for detailed monitoring:**

```python
# Enable detailed logging to see all commands and responses
config = CommunicationConfig(verbose=True)
api = ChemstationAPI(config)

# Alternative: Monitor communication files directly (PowerShell)
Get-Content "communication_files\command" -Wait
```

**Q: Občas vypadává komunikace mezi pythonem a Chemstationem. Čím je to způsobeno?**

**A: Výpadky komunikace byli pozorovány v určitých případech:**

1. **Po spuštění příkazu se v chmestationu objeví errorová tabulka**
    - Může se jednat o spuštění metody v době kdy kdy ji ještě běží metoda
    - Nesplnění timeoutu u příkazu send -> vyzkoušení vytvořeného příkazu a případné zvýšení timeoutu (viz příkaz validation.get_vialtable()), kde je u příkazu send nastaven vyšší timeout, jelikož provádění makra trvá delší dobu
    - po vypnutí errorové tabulky se může pokračovat dále
    - před spuštěním příkazů je potřeba předřadit validace aby se daný příkaz spustil ve vhodnou dobu

2. **Zadrhnutí komunikace**
    - U některých příkazů, které se volají velmi rychle po sobě ve smyčce se může stát je občas se nedostane odpověď
    - Tato situace nastávala u příkazu system.status(), kdy se při zjištování statusu občas nedostala odpověď a nastala chyba -> v příkazu je zavedený zaveden cyklus s try, kdy pokud se 3 nepodaří získat odpoveď, tak se až poté zobrazí chyba
    - V tomto případě se může pokračovat, stačí skript obnovit

### Custom ChemStation Commands

**Q: Can I send custom commands directly to ChemStation?**

**A: Yes, use the send() method for any valid ChemStation command:**

```python
# Read current oven temperature
response = api.send('response$ = VAL$(ObjHdrVal(RCCE1Status[1], "Temperature_actual"))')
print(f"Current oven temperature: {response}°C")

# Get method path
method_path = api.send("response$ = _METHPATH$")
print(f"Active method: {method_path}")
```

## Capillary Electrophoresis Operations

### Vial Loading Issues

**Q: Unable to load vials into the carousel**

**A: Vial loading failures typically occur for two main reasons:**

**System State Issues:**
The CE system may not be in a state that allows carousel operation. Vial loading is blocked when the system is in certain states to prevent operational conflicts:

- **IDLE state**: Normal operation - carousel accessible    
- **RUN state**: Analysis in progress - carousel may be locked
- **Other states**: Carousel typically locked for safety
- **Apply pressure in run**: Pokud je kdykoliv aplikován tlak, i během runu v metodě (přídavný tlak v analýze), tak je carousel zablokovaný a nelze použít

**Solution:** Implement state checking in your workflows:
```python
# Wait for appropriate system state before vial operations
while not api.is_carousel_available():
    time.sleep(5)  # Wait for system to reach appropriate state

# Then proceed with vial loading
carousel.load_vial(position=1)
```

**Missing Vial Validation:**
The system cannot locate the specified vial in the carousel.

**Solution:** Implement vial validation at workflow start:
```python
# Validate all required vials are present before starting
required_positions = [1, 2, 3, 5, 8]
missing_vials = carousel.validate_vials(required_positions)
if missing_vials:
    raise ValueError(f"Missing vials at positions: {missing_vials}")
```

## Method Configuration

### Modifying Method Parameters

**Q: Can I modify method parameters like temperature, voltage, etc. programmatically?**

**A: Yes, method parameters can be modified using ChemStation registry commands:**

Method parameters are stored in RC{module}Method[1] registers and can be modified directly:

```python
# Example: Modify separation voltage
api.send('SetObjHdrVal RCCE1Method[1], "Voltage", 10') tohle se musí opravit

```

Při zkoumání RC.Net logu (viz kapitola chemstation Macros 7. ""tady by bylo dobré udělat křířový odkaz"") bylo objeveno, že při změně parametrů metody se objevý příkazy pro jejich úpravu a při zadání příkazů se parametry upravili. Ovšem tento postup nebyl nijak testován.

**Additional Resources:**
- See tutorial/chemstation_scripting section on Registry RCNET for comprehensive parameter lists
- Reference implementation: [HPLC Method Optimization GUI](https://github.com/Bourne-Group/HPLCMethodOptimisationGUI/blob/main/MACROS(1)/editMeth.MAC)

## Sequential injection components

### Add conponents

**Q: Lze integravat další komponenty, tkeré nejsou součástí (míchadélka, pumpy, ...)?**

**A: Ano, do k´du lze přidal další komponenty:**

- V části SIA_API/Core je polečný komunikační rozhraní pro odesílání a příjmíní příkazů z COM portu, a které většinou komunikují SI komponenty jako mohou být pumpy, ventily nebo mikrocontrolery (Arduino, ESP32)
- Pro přidání dalších částí je nutné zjistit příkazy pomocí kterých se ovládají funkce daných komponent. Také je nutné jejich otestování před nasazením a správným nastavením komuikačního rozhraní.
- Současné ovládání a vytvořené moduly vznikly ze zdorjového k´du progranu [CocoSoft](https://link.springer.com/article/10.1007/s00216-015-8834-8) 7.2, pomocí kterého šlo ovládat i další komponenty. Bohužel v dnešní době již néní přístupný


## Syringe Operation

### syringe Volume Management

**Q: Getting syringe volume tracking errors**

**A: The API automatically tracks syringe volume, but errors can occur:**

```python
# Check current syringe volume in počítadlo
syringe.print_volume_in_syringe()

# Reset volume tracking if needed
syringe.dispense()  # Empty syringe completely and reset internal counter

# Or
syringe.get_actual_volume() # Vrácení naátého objemu ve stříkačce a přepsání počítadla

# Or perform complete reinitialization
syringe.initialize()
```


## Troubleshooting Guide

### Systematic Diagnosis Approach

When encountering issues, follow this diagnostic sequence:

**1. Verify Physical Connections**
- Confirm power status on all devices
- Check cable connections and COM port assignments
- Test basic communication with each component

**2. Validate Software Prerequisites**
- ChemStation running and responsive
- Required macros loaded and active
- All specified vials present in carousel
- Target methods exist and are accessible

**3. Analyze Error Messages**
- Note specific exception types and error codes
- Look for recurring error patterns
- Enable verbose mode for detailed diagnostics

**4. Component-Level Testing**
```python
# Test individual components in isolation
try:
    syringe.initialize()
    print("✓ syringe communication OK")
except Exception as e:
    print(f"✗ syringe error: {e}")

try:
    valve.position(1)
    print("✓ Valve communication OK")
except Exception as e:
    print(f"✗ Valve error: {e}")

try:
    response = api.send("response$ = _METHPATH$")
    print(f"✓ ChemStation communication OK: {response}")
except Exception as e:
    print(f"✗ ChemStation error: {e}")
```

### Common Issues Quick Reference

**Most frequent problems and solutions:**

1. **ChemStation macro not running** → Reload macro in ChemStation command line
2. **Incorrect COM port configuration** → Use device manager to verify port assignments  
3. **Missing vials or methods** → Implement validation checks at workflow start
4. **Timeout settings too short** → Increase timeout values for complex operations
5. **Volume tracking errors** → Reset syringe and reinitialize volume counter

## Getting Support

### Available Resources

- **GitHub Issues**: Report bugs, request features, and track development
- **Documentation**: Comprehensive guides covering all package functionality
- **Tutorial Examples**: Working code examples for common workflows

### Reporting Issues Effectively

When requesting support, please include:

- **Environment Details**: Python version, package version, operating system
- **Hardware Configuration**: CE model, SIA components, COM port assignments  
- **Error Information**: Complete error messages and stack traces
- **Minimal Example**: Simplified code that reproduces the issue
- **Context**: What you were trying to accomplish and what happened instead

---

!!! tip "Quick Resolution Tips"
    
    **90% of issues stem from these common causes:**
    
    1. **ChemStation macro not properly loaded or running**
    2. **COM port conflicts or incorrect assignments** 
    3. **Missing physical components (vials, methods)**
    4. **Insufficient timeout values for complex operations**
    
    **Always check these fundamentals first before diving into complex troubleshooting!**