# Implementing the Solovay-Kitaev algorithm

### Submitted to [CDL Quantum](https://www.creativedestructionlab.com/streams/quantum/) Hackathon 2021 by Alan Robertson and Yuval Sanders for [Quantum Oracles](https://vimeo.com/571477316/c26fa92407).

The Solovay-Kitaev theorem is a foundational result in quantum computing. The theorem states, roughly, that any single-qubit operation can be approximated with a fairly short sequence (i.e. polylogarithmic in target error) of basic single-qubit gates. Quantum algorithms researchers frequently appeal to the theorem in order to justify a unit cost for single-qubit operations such as those in the quantum Fourier transform.

The standard reference for the theorem is a paper written by Dawson and Nielsen in 2005 ([published version](https://dl.acm.org/doi/10.5555/2011679.2011685), [arXiv version](https://arxiv.org/abs/quant-ph/0505030)). In that paper, Dawson and Nielsen (hereafter [DN05]) offer a proof of the theorem in the form of an *algorithm*. As implied justification, [DN05] offer the following quote from Knuth:

>I have been impressed by numerous instances of mathematical theories that are really about particular algorithms; these theories are typically formulated in mathematical terms that are much more cumbersome and less natural than the equivalent formulation today’s computer scientists would use.

Dawson and Nielsen were prescient. As quantum technology develops, there is a rapidly growing need to assess the power of quantum computers. Current approaches take one of two forms: either
1. researchers (usually academic) carry out a highly technical asymptotic analysis and look for quantum outperformance relative to classical, or
2. researchers (frequently corporate) seek quantum circuits that could be run on specific, imperfect hardware.

Both approaches have their merits and drawbacks. Asymptotic analyses show beyond most reasonable doubt that there is some kind of advantage to using a quantum computer over classical, but the window for doubt includes open questions about the overheads incurred by specific quantum architectures. One specific example is [the famous question of computational overheads incurred when implementing quantum random access memory](https://doi.org/10.1088/1367-2630/17/12/123010).

On the other hand, the only long-term value to be had in quantum computing must outlive techniques that rely on quirks of today's technology (e.g. the quantum-annealing-based techniques of DWave) or the relative underdevelopment of classical algorithms for esoteric problems natural to quantum hardware (e.g. the 'quantum supremacy' experiments of recent years).

At Quantum Oracles, we believe that the future of quantum computing research and development requires thorough and rigorous resource estimation for quantum computer use cases. This resource estimation must say not only how expensive it would be to execute a quantum algorithm on specific hardware, but also how the cost of that quantum algorithm would scale as technology improves.

Like it or not, there is no clear evidence that today's quantum computing technology does anything that could not be reasonably simulated on a decent classical computer, at least given a few months of focussed research. We should think of quantum technology development as a race between quantum and classical, and we should remember the tale of the tortoise and the hare. The hare should beat the tortoise, but can only do so with consistent effort.

To apply consistent effort, we need clear milestones for quantum computer capabilities that pertain to real-world use cases. This requires scalable resource estimation of quantum computer use-cases, and that scalable resource estimation will take place on classical computers for the foreseeable future. It is therefore imperative for the future of the field that we commit to implementing core resource estimation techniques as software packages.

This submission to CDL Quantum constitutes a proof of concept for the idea. Despite the foundational nature of the Solovay-Kitaev theorem and the central relevance of the algorithm described in [DN05], there remains no reference code that can be incorporated into the various software projects being developed by industry players like Xanadu, Zapata, Rigetti, and IBM.

The code contained in this project is very much a work in progress, and is frozen at this point due to the time constraints of the hackathon event. The current implementation is not tested and is likely quite buggy. The authors fully intend to develop the code much further in order to ensure interoperability with the lower-level software being developed by the quantum industry. By doing so, we intend to demonstrate the value of implementing high-level quantum algorithmic techniques in professionally developed software packages.

The most immediate use-case we see is in resource estimation as needed by stakeholders in the quantum industry for milestone and benchmark development, but our ambitions range far beyond the immediate term. We envision a world in which end users of quantum computers can design their own, proprietary quantum algorithms without having to go through the costly tedium of hand-crafting low-level quantum circuits that accomplish the desired task. In short, we envision the quantum equivalent of the [C programming language](https://en.wikipedia.org/wiki/C_(programming_language)). We intend to build it.

[DN05]: https://arxiv.org/abs/quant-ph/0505030