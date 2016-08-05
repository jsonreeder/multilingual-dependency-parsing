class Transition(object):
    """
    This class defines a set of transitions which are applied to a
    configuration to get the next configuration.
    """
    # Define set of transitions
    LEFT_ARC = 'LEFTARC'
    RIGHT_ARC = 'RIGHTARC'
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'

    def __init__(self):
        raise ValueError('Do not construct this object!')

    @staticmethod
    def left_arc(conf, relation):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """

        # Precondition: "wi" not already the dependent of another word
        # TODO: Add if statement for precondition

        # Add to arcs

        # Remove from stack

        raise NotImplementedError('Please implement left_arc!')
        return -1

    @staticmethod
    def right_arc(conf, relation):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """

        # Precondition: Neither the stack nor the buffer are empty
        if not conf.buffer or not conf.stack:
            return -1

        # You get this one for free! Use it as an example.

        idx_wi = conf.stack[-1]
        idx_wj = conf.buffer.pop(0)

        conf.stack.append(idx_wj)
        conf.arcs.append((idx_wi, relation, idx_wj))

    @staticmethod
    def reduce(conf):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """

        # Precondition: Word must be the dependent of another word
        # TODO: Add if statement for precondition

        raise NotImplementedError('Please implement reduce!')
        return -1

    @staticmethod
    def shift(conf):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """

        # Precondition: Neither the stack nor the buffer are empty
        if not conf.buffer or not conf.stack:
            return -1

        # Word at the top of the buffer moved to the stack
        idx_wj = conf.buffer.pop(0)
        conf.stack.append(idx_wj)
